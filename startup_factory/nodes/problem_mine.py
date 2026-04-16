from __future__ import annotations

import json

from ..config import StructuredLLM
from ..schemas import ProblemMiningResult
from ..state import WorkflowState
from . import load_prompt


def build_problem_mine_node(llm: StructuredLLM):
    system_prompt = load_prompt("problem_mine.txt")

    def problem_mine(state: WorkflowState) -> WorkflowState:
        user_prompt = json.dumps(
            {
                "brief": state["user_brief"],
                "constraints": state.get("constraints") or {},
                "industries": [
                    industry.model_dump() for industry in state.get("industries", [])
                ],
            },
            indent=2,
        )
        result = llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_model=ProblemMiningResult,
        )
        return {"problems": result.problems}

    return problem_mine
