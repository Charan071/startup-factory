from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .config import StructuredLLM
from .nodes.critique_ideas import build_critique_ideas_node
from .nodes.finalize_output import build_finalize_output_node
from .nodes.generate_ideas import build_generate_ideas_node
from .nodes.industry_scan import build_industry_scan_node
from .nodes.problem_mine import build_problem_mine_node
from .nodes.score_ideas import build_score_ideas_node
from .schemas import FinalReport, RunRequest
from .services.llm import OpenAIStructuredLLM
from .state import WorkflowState


def build_graph(llm: StructuredLLM | None = None):
    llm = llm or OpenAIStructuredLLM()

    graph = StateGraph(WorkflowState)
    graph.add_node("industry_scan", build_industry_scan_node(llm))
    graph.add_node("problem_mine", build_problem_mine_node(llm))
    graph.add_node("generate_ideas", build_generate_ideas_node(llm))
    graph.add_node("critique_ideas", build_critique_ideas_node(llm))
    graph.add_node("score_ideas", build_score_ideas_node(llm))
    graph.add_node("finalize_output", build_finalize_output_node())

    graph.add_edge(START, "industry_scan")
    graph.add_edge("industry_scan", "problem_mine")
    graph.add_edge("problem_mine", "generate_ideas")
    graph.add_edge("generate_ideas", "critique_ideas")
    graph.add_edge("critique_ideas", "score_ideas")
    graph.add_edge("score_ideas", "finalize_output")
    graph.add_edge("finalize_output", END)
    return graph.compile()


def run_startup_factory(
    request: RunRequest,
    llm: StructuredLLM | None = None,
) -> FinalReport:
    graph = build_graph(llm=llm)
    result = graph.invoke(
        {
            "user_brief": request.brief,
            "constraints": request.constraints or {},
            "top_k": request.top_k,
        }
    )
    return FinalReport.model_validate(result["final_output"])
