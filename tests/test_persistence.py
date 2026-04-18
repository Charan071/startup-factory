from pathlib import Path

from startup_factory.schemas import FinalReport, RunRequest
from startup_factory.services.persistence import ArtifactStore


def test_artifact_store_saves_and_loads_run(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    request = RunRequest(brief="Find startup ideas in logistics.", top_k=1)
    saved = store.save_run(
        request=request,
        report=FinalReport(brief=request.brief, top_ideas=[]),
    )
    loaded = store.load_run(saved.run_id)

    assert Path(saved.artifact_path).exists()
    assert saved.artifact_name
    assert saved.created_at is not None
    assert loaded.saved_run.run_id == saved.run_id
    assert loaded.request.brief == request.brief
    assert loaded.report.brief == request.brief


def test_artifact_store_lists_run_summaries(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    request = RunRequest(brief="Find startup ideas in logistics.", top_k=1)
    store.save_run(
        request=request,
        report=FinalReport(brief=request.brief, top_ideas=[]),
    )

    runs = store.list_runs()

    assert len(runs) == 1
    assert runs[0].brief == request.brief
    assert runs[0].artifact_name.endswith(".json")
