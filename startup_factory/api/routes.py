from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from ..schemas import (
    RunExecutionResult,
    RunListResponse,
    RunRequest,
    RunSummary,
    SavedRunRecord,
)
from ..services.runner import (
    execute_startup_factory,
    list_saved_runs,
    load_saved_run,
    load_saved_run_summary,
)


def build_router() -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.post("/runs", response_model=RunExecutionResult)
    def create_run(request: RunRequest) -> RunExecutionResult:
        return execute_startup_factory(request)

    @router.get("/runs", response_model=RunListResponse)
    def get_runs(limit: int = Query(default=20, ge=1, le=100)) -> RunListResponse:
        return list_saved_runs(limit=limit)

    @router.get("/runs/{run_id}", response_model=SavedRunRecord)
    def get_run(run_id: str) -> SavedRunRecord:
        try:
            return load_saved_run(run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @router.get("/runs/{run_id}/summary", response_model=RunSummary)
    def get_run_summary(run_id: str) -> RunSummary:
        try:
            return load_saved_run_summary(run_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return router
