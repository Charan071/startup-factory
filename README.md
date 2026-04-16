# LangChain Deep Agents Playground

This repo contains a small `LangGraph` PDF Q&A example, a versioned planning area, and a new `startup_factory` CLI for generating ranked B2B startup ideas.

## In This Repo

- `PDF Q&A Assistant`: a small, study-friendly `LangGraph` example in [app.py](app.py)
- `Startup Factory Architecture`: the planned system design in [docs/startup-factory-architecture.md](docs/startup-factory-architecture.md)
- `Latest Plan`: the current implementation plan in [docs/plans/2026-04-17-startup-factory-v1.md](docs/plans/2026-04-17-startup-factory-v1.md)
- `Plans Index`: versioned plan history in [docs/plans/index.md](docs/plans/index.md)
- `Issues Index`: markdown backlog in [issues/index.md](issues/index.md)

## Startup Factory Plan

The planned startup-idea system is `LangGraph`-first, with optional `deepagents` used later inside research-heavy nodes. See the architecture doc for:

- system architecture
- file architecture
- tech stack
- node responsibilities
- phase-by-phase build plan

## Startup Factory CLI

The new V1 `startup_factory` package is a CLI-first startup idea generator that:

1. scans for inefficient industries
2. mines narrow B2B problems
3. generates feasible software ideas
4. critiques each idea
5. scores and ranks the best options

Run it with:

```powershell
.\.venv\Scripts\python -m startup_factory.cli --brief "Find vertical SaaS ideas in logistics" --top-k 3
```

Optional JSON output:

```powershell
.\.venv\Scripts\python -m startup_factory.cli --brief "Find vertical SaaS ideas in logistics" --json
```

The CLI uses:

- `OPENAI_API_KEY` for model-backed runs
- optional LangSmith env vars for tracing:
  - `LANGSMITH_TRACING`
  - `LANGSMITH_ENDPOINT`
  - `LANGSMITH_API_KEY`
  - `LANGSMITH_PROJECT`

## PDF Q&A Assistant

A small, study-friendly PDF question-answering assistant built with `LangGraph`.

It shows the basic retrieval-augmented generation (RAG) pattern:

1. Read a PDF
2. Split it into chunks
3. Retrieve the most relevant chunks for a question
4. Ask an LLM to answer using only that context

This project intentionally keeps the stack light so the architecture is easy to learn.

## Why this project is a good starting point

- It solves a real problem: asking questions over long PDFs.
- It introduces the core ideas behind agent systems without overwhelming you.
- It uses `LangGraph`, so you can see explicit state and flow instead of hidden magic.

## High-Level Architecture

The assistant has four stages:

1. `load_pdf`
   Reads the PDF and extracts page text.
2. `chunk_pdf`
   Splits the text into smaller overlapping chunks.
3. `retrieve_context`
   Scores chunks against the user question and selects the best matches.
4. `generate_answer`
   Sends the question and retrieved context to the LLM.

`LangGraph` manages the state that moves through those stages.

## Flow

1. User provides a PDF path and a question.
2. The graph loads the PDF text.
3. The text is chunked into manageable sections.
4. The assistant ranks chunks by keyword overlap with the question.
5. The best chunks are passed into the answer step.
6. If `OPENAI_API_KEY` is configured, the app asks the model for an answer grounded in the retrieved context.
7. If no API key is configured, the app returns the best-matching passages so you can still inspect what retrieval found.

## Files

- `app.py`: main LangGraph app
- `requirements.txt`: Python dependencies for the virtual environment

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```bash
python app.py --pdf path/to/file.pdf --question "What are the main arguments?"
```

Or from the virtual environment explicitly:

```powershell
.venv\Scripts\python app.py --pdf .\your-file.pdf --question "What does this document say about pricing?"
```

If you want model-generated answers, set:

```bash
set OPENAI_API_KEY=your_key
```

On PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key"
```

This project also reads a local `.env` file automatically, so you can store:

```dotenv
OPENAI_API_KEY=your_key
```

## What You Learn From This

- How to model an AI workflow as a graph
- How RAG works at a practical level
- Why retrieval improves accuracy on long documents
- How state moves between nodes in `LangGraph`

## Natural Next Upgrades

- Replace keyword retrieval with embeddings
- Persist chunks in a vector store
- Add a chat UI
- Support follow-up questions over the same PDF
- Add citations by page number
- Turn the answer step into a tool-using deep agent
