from __future__ import annotations

from typing import TypedDict

from .schemas import (
    CritiqueFeedback,
    FinalReport,
    IdeaDraft,
    IdeaScore,
    IndustryFinding,
    ProblemFinding,
    StartupIdea,
)


class WorkflowState(TypedDict, total=False):
    user_brief: str
    constraints: dict[str, str] | None
    top_k: int
    industries: list[IndustryFinding]
    problems: list[ProblemFinding]
    ideas: list[IdeaDraft]
    critiques: list[CritiqueFeedback]
    scores: list[IdeaScore]
    ranked_ideas: list[StartupIdea]
    final_output: FinalReport
