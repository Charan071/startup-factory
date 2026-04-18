from fastapi.testclient import TestClient

from startup_factory.api.main import create_app
from startup_factory.schemas import (
    FinalReport,
    RunExecutionResult,
    SavedRun,
    ScoreBreakdown,
    StartupIdea,
)


def make_execution_result():
    return RunExecutionResult(
        report=FinalReport(
            brief="Find vertical SaaS ideas in logistics.",
            top_ideas=[
                StartupIdea(
                    title="FreightInvoiceOps",
                    industry="Logistics",
                    problem="Manual invoice reconciliation slows collections.",
                    solution="Automate invoice matching and approval routing.",
                    icp="Mid-market freight brokerages",
                    mvp="Invoice ingestion and discrepancy queue",
                    gtm="Outbound to finance leaders",
                    critic_summary="High pain, but integration depth matters.",
                    score=8.8,
                    score_breakdown=ScoreBreakdown(
                        urgency=9,
                        willingness_to_pay=9,
                        feasibility=8,
                        defensibility=7,
                    ),
                )
            ],
        )
    )


def test_health_endpoint():
    client = TestClient(create_app())
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_run_endpoint(monkeypatch):
    monkeypatch.setattr(
        "startup_factory.api.routes.execute_startup_factory",
        lambda request: make_execution_result().model_copy(
            update={
                "saved_run": SavedRun(
                    run_id="run_123",
                    artifact_path="artifacts/startup_factory/2026-04-18/run.json",
                    artifact_name="run.json",
                )
            }
        ),
    )

    client = TestClient(create_app())
    response = client.post(
        "/api/v1/runs",
        json={"brief": "Find vertical SaaS ideas in logistics.", "top_k": 1},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["report"]["top_ideas"][0]["title"] == "FreightInvoiceOps"
    assert payload["saved_run"]["run_id"] == "run_123"


def test_list_runs_endpoint(monkeypatch):
    monkeypatch.setattr(
        "startup_factory.api.routes.list_saved_runs",
        lambda limit=20: {
            "runs": [
                {
                    "run_id": "run_123",
                    "created_at": "2026-04-18T13:30:32.480157Z",
                    "brief": "Find vertical SaaS ideas in logistics.",
                    "artifact_name": "run.json",
                    "top_idea_titles": ["FreightInvoiceOps"],
                    "top_score": 8.8,
                }
            ]
        },
    )

    client = TestClient(create_app())
    response = client.get("/api/v1/runs")

    assert response.status_code == 200
    assert response.json()["runs"][0]["run_id"] == "run_123"


def test_run_summary_endpoint(monkeypatch):
    monkeypatch.setattr(
        "startup_factory.api.routes.load_saved_run_summary",
        lambda run_id: {
            "run_id": run_id,
            "created_at": "2026-04-18T13:30:32.480157Z",
            "brief": "Find vertical SaaS ideas in logistics.",
            "artifact_name": "run.json",
            "top_idea_titles": ["FreightInvoiceOps"],
            "top_score": 8.8,
        },
    )

    client = TestClient(create_app())
    response = client.get("/api/v1/runs/run_123/summary")

    assert response.status_code == 200
    assert response.json()["run_id"] == "run_123"
