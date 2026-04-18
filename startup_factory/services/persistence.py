from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..config import load_settings
from ..schemas import (
    FinalReport,
    RunRequest,
    RunSummary,
    SavedRun,
    SavedRunRecord,
)


def slugify(value: str, *, max_length: int = 48) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    slug = slug or "startup-factory-run"
    return slug[:max_length].rstrip("-") or "startup-factory-run"


class ArtifactStore:
    def __init__(self, base_dir: str | Path | None = None):
        settings = load_settings()
        root = Path(base_dir) if base_dir is not None else settings.artifact_dir
        self.base_dir = Path(root)

    def save_run(
        self,
        *,
        request: RunRequest,
        report: FinalReport,
    ) -> SavedRun:
        timestamp = datetime.now(timezone.utc)
        run_id = uuid4().hex
        slug = slugify(request.brief)
        dated_dir = self.base_dir / timestamp.strftime("%Y-%m-%d")
        dated_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = dated_dir / f"{timestamp.strftime('%H%M%S')}-{slug}-{run_id}.json"
        saved_run = SavedRun(
            run_id=run_id,
            artifact_path=str(artifact_path),
            artifact_name=artifact_path.name,
            created_at=timestamp,
        )
        record = SavedRunRecord(
            saved_run=saved_run,
            request=request,
            report=report,
        )
        artifact_path.write_text(
            json.dumps(record.model_dump(mode="json"), indent=2),
            encoding="utf-8",
        )
        return saved_run

    def load_run(self, run_id: str) -> SavedRunRecord:
        matches = list(self.base_dir.rglob(f"*{run_id}.json"))
        if not matches:
            raise FileNotFoundError(f"No saved run found for run_id '{run_id}'.")
        if len(matches) > 1:
            raise RuntimeError(
                f"Multiple saved runs matched run_id '{run_id}'."
            )
        return SavedRunRecord.model_validate_json(
            matches[0].read_text(encoding="utf-8")
        )

    def list_runs(self, limit: int = 20) -> list[RunSummary]:
        if not self.base_dir.exists():
            return []

        runs: list[RunSummary] = []
        for artifact_path in sorted(
            self.base_dir.rglob("*.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        ):
            record = SavedRunRecord.model_validate_json(
                artifact_path.read_text(encoding="utf-8")
            )
            created_at = (
                record.saved_run.created_at
                or record.report.generated_at
                or datetime.fromtimestamp(
                    artifact_path.stat().st_mtime,
                    tz=timezone.utc,
                )
            )
            runs.append(
                RunSummary(
                    run_id=record.saved_run.run_id,
                    created_at=created_at,
                    brief=record.request.brief,
                    artifact_name=(
                        record.saved_run.artifact_name or artifact_path.name
                    ),
                    top_idea_titles=[
                        idea.title for idea in record.report.top_ideas[:3]
                    ],
                    top_score=(
                        record.report.top_ideas[0].score
                        if record.report.top_ideas
                        else None
                    ),
                )
            )
            if len(runs) >= limit:
                break

        return runs

    def load_run_summary(self, run_id: str) -> RunSummary:
        record = self.load_run(run_id)
        artifact_path = Path(record.saved_run.artifact_path)
        created_at = (
            record.saved_run.created_at
            or record.report.generated_at
            or datetime.now(timezone.utc)
        )
        return RunSummary(
            run_id=record.saved_run.run_id,
            created_at=created_at,
            brief=record.request.brief,
            artifact_name=record.saved_run.artifact_name or artifact_path.name,
            top_idea_titles=[idea.title for idea in record.report.top_ideas[:3]],
            top_score=(
                record.report.top_ideas[0].score
                if record.report.top_ideas
                else None
            ),
        )
