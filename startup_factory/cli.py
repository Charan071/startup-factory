from __future__ import annotations

import argparse
import sys

from pydantic import ValidationError

from .graph import run_startup_factory
from .schemas import FinalReport, RunRequest


def parse_constraints(items: list[str]) -> dict[str, str] | None:
    if not items:
        return None

    constraints: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(
                f"Invalid constraint '{item}'. Expected KEY=VALUE format."
            )
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError(
                f"Invalid constraint '{item}'. Expected KEY=VALUE format."
            )
        constraints[key] = value
    return constraints


def render_markdown(report: FinalReport) -> str:
    lines = [
        "# Startup Factory Report",
        "",
        f"- Generated: {report.generated_at.isoformat()}",
        f"- Brief: {report.brief}",
        "",
    ]

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate ranked B2B startup ideas from a brief."
    )
    parser.add_argument("--brief", required=True, help="Startup search brief")
    parser.add_argument("--top-k", type=int, default=3, help="Ideas to return")
    parser.add_argument(
        "--constraint",
        action="append",
        default=[],
        help="Repeatable KEY=VALUE constraint",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON instead of markdown",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        constraints = parse_constraints(args.constraint)
        request = RunRequest(
            brief=args.brief,
            top_k=args.top_k,
            constraints=constraints,
        )
        report = run_startup_factory(request)
    except (RuntimeError, ValueError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
