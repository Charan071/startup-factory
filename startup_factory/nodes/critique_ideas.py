from __future__ import annotations

import json

from ..config import StructuredLLM
from ..schemas import CritiqueResult
from ..state import WorkflowState
from . import load_prompt


def build_critique_ideas_node(llm: StructuredLLM):
    system_prompt = load_prompt("critique_ideas.txt")

    def critique_ideas(state: WorkflowState) -> WorkflowState:
        user_prompt = json.dumps(
            {
                "brief": state["user_brief"],
                "ideas": [idea.model_dump() for idea in state.get("ideas", [])],
            },
            indent=2,
        )
        result = llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_model=CritiqueResult,
        )
        return {"critiques": result.critiques}

    return critique_ideas
