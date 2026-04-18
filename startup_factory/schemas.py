from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RunRequest(StrictModel):
    brief: str
    constraints: dict[str, str] | None = None
    top_k: int = Field(default=3, ge=1, le=10)

    @field_validator("brief")
    @classmethod
    def validate_brief(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("brief must not be blank")
        return cleaned


class IndustryFinding(StrictModel):
    name: str
    inefficiency: str
    why_now: str


class ProblemFinding(StrictModel):
    id: str
    industry: str
    problem: str
    buyer_role: str
    pain_summary: str


class IdeaDraft(StrictModel):
    id: str
    title: str
    industry: str
    problem: str
    solution: str
    icp: str
    mvp: str
    gtm: str


class CritiqueFeedback(StrictModel):
    idea_id: str
    critic_summary: str
    fatal_risks: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)


class ScoreBreakdown(StrictModel):
    urgency: int = Field(ge=1, le=10)
    willingness_to_pay: int = Field(ge=1, le=10)
    feasibility: int = Field(ge=1, le=10)
    defensibility: int = Field(ge=1, le=10)


class IdeaScore(StrictModel):
    idea_id: str
    urgency: int = Field(ge=1, le=10)
    willingness_to_pay: int = Field(ge=1, le=10)
    feasibility: int = Field(ge=1, le=10)
    defensibility: int = Field(ge=1, le=10)
    overall: float = Field(ge=0, le=10)
    reasoning: str


class StartupIdea(StrictModel):
    title: str
    industry: str
    problem: str
    solution: str
    icp: str
    mvp: str
    gtm: str
    critic_summary: str
    score: float = Field(ge=0, le=10)
    score_breakdown: ScoreBreakdown


class FinalReport(StrictModel):
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    brief: str
    top_ideas: list[StartupIdea]


class SavedRun(StrictModel):
    run_id: str
    artifact_path: str
    artifact_name: str | None = None
    created_at: datetime | None = None


class RunSummary(StrictModel):
    run_id: str
    created_at: datetime
    brief: str
    artifact_name: str
    top_idea_titles: list[str]
    top_score: float | None = None


class RunListResponse(StrictModel):
    runs: list[RunSummary]


class RunExecutionResult(StrictModel):
    report: FinalReport
    saved_run: SavedRun | None = None


class SavedRunRecord(StrictModel):
    saved_run: SavedRun
    request: RunRequest
    report: FinalReport


class IndustryScanResult(StrictModel):
    industries: list[IndustryFinding]


class ProblemMiningResult(StrictModel):
    problems: list[ProblemFinding]


class IdeaGenerationResult(StrictModel):
    ideas: list[IdeaDraft]


class CritiqueResult(StrictModel):
    critiques: list[CritiqueFeedback]


class ScoreResult(StrictModel):
    scores: list[IdeaScore]
