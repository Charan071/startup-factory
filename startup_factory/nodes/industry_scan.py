from __future__ import annotations

import json

from ..config import StructuredLLM
from ..schemas import IndustryScanResult
from ..state import WorkflowState
from . import load_prompt


def build_industry_scan_node(llm: StructuredLLM):
    system_prompt = load_prompt("industry_scan.txt")

    def industry_scan(state: WorkflowState) -> WorkflowState:
        user_prompt = json.dumps(
            {
                "brief": state["user_brief"],
                "constraints": state.get("constraints") or {},
            },
            indent=2,
        )
        result = llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            output_model=IndustryScanResult,
        )
        return {"industries": result.industries}

    return industry_scan
