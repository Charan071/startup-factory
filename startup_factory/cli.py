from __future__ import annotations

import argparse
import sys

from pydantic import ValidationError

from .schemas import RunRequest
from .services.formatting import render_markdown
from .services.runner import execute_startup_factory


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
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save a JSON run artifact to disk",
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
        result = execute_startup_factory(
            request,
            save_artifact=not args.no_save,
        )
    except (RuntimeError, ValueError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(result.model_dump_json(indent=2))
    else:
        print(render_markdown(result.report, result.saved_run), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
