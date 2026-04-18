from __future__ import annotations

from ..graph import build_graph
from ..schemas import (
    FinalReport,
    RunExecutionResult,
    RunListResponse,
    RunRequest,
    RunSummary,
    SavedRunRecord,
)
from .llm import OpenAIStructuredLLM, StructuredLLM
from .persistence import ArtifactStore


def execute_startup_factory(
    request: RunRequest,
    *,
    llm: StructuredLLM | None = None,
    artifact_store: ArtifactStore | None = None,
    save_artifact: bool = True,
) -> RunExecutionResult:
    graph = build_graph(llm=llm or OpenAIStructuredLLM())
    result = graph.invoke(
        {
            "user_brief": request.brief,
            "constraints": request.constraints or {},
            "top_k": request.top_k,
        }
    )
    report = FinalReport.model_validate(result["final_output"])

    saved_run = None
    if save_artifact:
        artifact_store = artifact_store or ArtifactStore()
        saved_run = artifact_store.save_run(request=request, report=report)

    return RunExecutionResult(report=report, saved_run=saved_run)


def load_saved_run(
    run_id: str,
    *,
    artifact_store: ArtifactStore | None = None,
) -> SavedRunRecord:
    artifact_store = artifact_store or ArtifactStore()
    return artifact_store.load_run(run_id)


def list_saved_runs(
    *,
    artifact_store: ArtifactStore | None = None,
    limit: int = 20,
) -> RunListResponse:
    artifact_store = artifact_store or ArtifactStore()
    return RunListResponse(runs=artifact_store.list_runs(limit=limit))


def load_saved_run_summary(
    run_id: str,
    *,
    artifact_store: ArtifactStore | None = None,
) -> RunSummary:
    artifact_store = artifact_store or ArtifactStore()
    return artifact_store.load_run_summary(run_id)
