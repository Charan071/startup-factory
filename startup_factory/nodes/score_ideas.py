from __future__ import annotations

import json

from ..config import StructuredLLM
from ..schemas import ScoreBreakdown, ScoreResult, StartupIdea
from ..state import WorkflowState
from . import load_prompt


def build_score_ideas_node(llm: StructuredLLM):
    system_prompt = load_prompt("score_ideas.txt")

    def score_ideas(state: WorkflowState) -> WorkflowState:
        user_prompt = json.dumps(
            {
                "brief": state["user_brief"],
                "ideas": [idea.model_dump() for idea in state.get("ideas", [])],
                "critiques": [
                    critique.model_dump()
                    for critique in state.get("critiques", [])
                ],
            },
            indent=2,
        )
        result = llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_model=ScoreResult,
        )

        critiques_by_id = {
            critique.idea_id: critique for critique in state.get("critiques", [])
        }
        scores_by_id = {score.idea_id: score for score in result.scores}

        ranked_ideas: list[StartupIdea] = []
        for idea in state.get("ideas", []):
            critique = critiques_by_id.get(idea.id)
            score = scores_by_id.get(idea.id)
            if critique is None or score is None:
                raise RuntimeError(
                    f"Missing critique or score for idea '{idea.id}'."
                )

            ranked_ideas.append(
                StartupIdea(
                    title=idea.title,
                    industry=idea.industry,
                    problem=idea.problem,
                    solution=idea.solution,
                    icp=idea.icp,
                    mvp=idea.mvp,
                    gtm=idea.gtm,
                    critic_summary=critique.critic_summary,
                    score=score.overall,
                    score_breakdown=ScoreBreakdown(
                        urgency=score.urgency,
                        willingness_to_pay=score.willingness_to_pay,
                        feasibility=score.feasibility,
                        defensibility=score.defensibility,
                    ),
                )
            )

        ranked_ideas.sort(key=lambda item: (-item.score, item.title.lower()))
        top_k = state.get("top_k", 3)
        return {
            "scores": result.scores,
            "ranked_ideas": ranked_ideas[:top_k],
        }

    return score_ideas
