from __future__ import annotations

from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")
