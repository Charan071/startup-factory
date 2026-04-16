from __future__ import annotations

from ..schemas import FinalReport
from ..state import WorkflowState


def build_finalize_output_node():
    def finalize_output(state: WorkflowState) -> WorkflowState:
        report = FinalReport(
            brief=state["user_brief"],
            top_ideas=state.get("ranked_ideas", []),
        )
        return {"final_output": report}

    return finalize_output
