from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from openai import OpenAI
from pypdf import PdfReader


class GraphState(TypedDict, total=False):
    pdf_path: str
    question: str
    pages: list[dict]
    chunks: list[dict]
    retrieved_chunks: list[dict]
    answer: str


def load_local_env_file(env_path: str = ".env") -> None:
    path = Path(env_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        # Keep shell-provided variables as the source of truth.
        os.environ.setdefault(key, value)


def find_local_pdfs(root: Path) -> list[Path]:
    return sorted(root.glob("*.pdf"))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    if not text:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)

    return chunks


def load_pdf(state: GraphState) -> GraphState:
    pdf_path = Path(state["pdf_path"])
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages: list[dict] = []

    for idx, page in enumerate(reader.pages, start=1):
        text = normalize_text(page.extract_text() or "")
        if text:
            pages.append({"page": idx, "text": text})

    if not pages:
        raise ValueError("No extractable text was found in the PDF.")

    return {"pages": pages}


def chunk_pdf(state: GraphState) -> GraphState:
    chunks: list[dict] = []

    for page in state.get("pages", []):
        for chunk_idx, text in enumerate(chunk_text(page["text"])):
            chunks.append(
                {
                    "page": page["page"],
                    "chunk_id": f"p{page['page']}-c{chunk_idx}",
                    "text": text,
                }
            )

    return {"chunks": chunks}


def score_chunk(question: str, chunk_text_value: str) -> int:
    question_tokens = tokenize(question)
    chunk_tokens = tokenize(chunk_text_value)
    return len(question_tokens.intersection(chunk_tokens))


def retrieve_context(state: GraphState) -> GraphState:
    question = state["question"]
    chunks = state.get("chunks", [])
    ranked = sorted(
        (
            {
                **chunk,
                "score": score_chunk(question, chunk["text"]),
            }
            for chunk in chunks
        ),
        key=lambda item: item["score"],
        reverse=True,
    )
    retrieved = [chunk for chunk in ranked[:4] if chunk["score"] > 0]
    if not retrieved:
        retrieved = ranked[:2]
    return {"retrieved_chunks": retrieved}


def build_context(chunks: list[dict]) -> str:
    parts = []
    for chunk in chunks:
        parts.append(
            f"[Page {chunk['page']} | {chunk['chunk_id']}]\n{chunk['text']}"
        )
    return "\n\n".join(parts)


def generate_answer(state: GraphState) -> GraphState:
    retrieved = state.get("retrieved_chunks", [])
    context = build_context(retrieved)
    question = state["question"]
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        preview = context[:2000] if context else "No matching context found."
        answer = (
            "OPENAI_API_KEY is not set, so here are the retrieved passages.\n\n"
            f"Question: {question}\n\n"
            f"Retrieved context:\n{preview}"
        )
        return {"answer": answer}

    client = OpenAI(api_key=api_key)
    prompt = (
        "You are a PDF question-answering assistant.\n"
        "Answer only from the provided context.\n"
        "If the answer is not in the context, say you do not have enough evidence.\n\n"
        f"Question:\n{question}\n\n"
        f"Context:\n{context}"
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return {"answer": response.output_text}


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("load_pdf", load_pdf)
    graph.add_node("chunk_pdf", chunk_pdf)
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "load_pdf")
    graph.add_edge("load_pdf", "chunk_pdf")
    graph.add_edge("chunk_pdf", "retrieve_context")
    graph.add_edge("retrieve_context", "generate_answer")
    graph.add_edge("generate_answer", END)
    return graph.compile()


def main() -> None:
    load_local_env_file()

    parser = argparse.ArgumentParser(description="Ask questions about a PDF.")
    parser.add_argument("--pdf", required=True, help="Path to the PDF file")
    parser.add_argument("--question", required=True, help="Question to ask")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        nearby_pdfs = find_local_pdfs(Path.cwd())
        if nearby_pdfs:
            print("\nPDFs available in this folder:")
            for candidate in nearby_pdfs:
                print(f"- {candidate.name}")
        print(
            "\nExample:\n"
            'python app.py --pdf .\\sample.pdf --question "What does the document say about LangGraph?"'
        )
        sys.exit(1)

    graph = build_graph()

    try:
        result = graph.invoke({"pdf_path": args.pdf, "question": args.question})
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    print("\n=== Answer ===\n")
    print(result["answer"])

    retrieved = result.get("retrieved_chunks", [])
    if retrieved:
        print("\n=== Sources ===\n")
        for chunk in retrieved:
            print(
                f"Page {chunk['page']} | {chunk['chunk_id']} | score={chunk['score']}"
            )


if __name__ == "__main__":
    main()
