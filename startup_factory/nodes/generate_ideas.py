from __future__ import annotations

import json

from ..config import StructuredLLM
from ..schemas import IdeaGenerationResult
from ..state import WorkflowState
from . import load_prompt


def build_generate_ideas_node(llm: StructuredLLM):
    system_prompt = load_prompt("generate_ideas.txt")

    def generate_ideas(state: WorkflowState) -> WorkflowState:
        user_prompt = json.dumps(
            {
                "brief": state["user_brief"],
                "constraints": state.get("constraints") or {},
                "problems": [
                    problem.model_dump() for problem in state.get("problems", [])
                ],
            },
            indent=2,
        )
        result = llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_model=IdeaGenerationResult,
        )
        return {"ideas": result.ideas}

    return generate_ideas
