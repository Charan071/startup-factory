from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class StructuredLLM(Protocol):
    def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        output_model: type[T],
    ) -> T:
        ...


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    openai_model: str = "gpt-4o-mini"
    artifact_dir: Path = Path("artifacts") / "startup_factory"
    cors_origins: tuple[str, ...] = (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    )


def load_settings(env_path: str = ".env") -> Settings:
    load_dotenv(dotenv_path=Path(env_path), override=False)
    artifact_dir = Path(
        os.getenv("STARTUP_FACTORY_ARTIFACT_DIR", "artifacts/startup_factory")
    )
    cors_origins_raw = os.getenv(
        "STARTUP_FACTORY_CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )
    cors_origins = tuple(
        origin.strip()
        for origin in cors_origins_raw.split(",")
        if origin.strip()
    )
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        artifact_dir=artifact_dir,
        cors_origins=cors_origins,
    )
