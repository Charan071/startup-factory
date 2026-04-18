from __future__ import annotations

from ..schemas import FinalReport, SavedRun


def render_markdown(report: FinalReport, saved_run: SavedRun | None = None) -> str:
    lines = [
        "# Startup Factory Report",
        "",
        f"- Generated: {report.generated_at.isoformat()}",
        f"- Brief: {report.brief}",
    ]

    if saved_run is not None:
        lines.extend(
            [
                f"- Run ID: {saved_run.run_id}",
                f"- Saved Artifact: {saved_run.artifact_path}",
            ]
        )

    lines.append("")

    for index, idea in enumerate(report.top_ideas, start=1):
        lines.extend(
            [
                f"## {index}. {idea.title}",
                f"- Industry: {idea.industry}",
                f"- Problem: {idea.problem}",
                f"- Solution: {idea.solution}",
                f"- ICP: {idea.icp}",
                f"- MVP: {idea.mvp}",
                f"- GTM: {idea.gtm}",
                f"- Critic Summary: {idea.critic_summary}",
                f"- Score: {idea.score:.1f}/10",
                (
                    "- Score Breakdown: "
                    f"urgency={idea.score_breakdown.urgency}, "
                    f"willingness_to_pay={idea.score_breakdown.willingness_to_pay}, "
                    f"feasibility={idea.score_breakdown.feasibility}, "
                    f"defensibility={idea.score_breakdown.defensibility}"
                ),
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"
