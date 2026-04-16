from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypeVar

import openai
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from pydantic import BaseModel, ValidationError

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


def load_settings(env_path: str = ".env") -> Settings:
    load_dotenv(dotenv_path=Path(env_path), override=False)
    return Settings(openai_api_key=os.getenv("OPENAI_API_KEY"))


class OpenAIStructuredLLM:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or load_settings()
        if not self.settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to your shell or .env before "
                "running startup_factory."
            )
        self.client = wrap_openai(
            openai.Client(api_key=self.settings.openai_api_key)
        )

    def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        output_model: type[T],
    ) -> T:
        response = self.client.chat.completions.create(
            model=self.settings.openai_model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenAI returned an empty response.")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Model returned invalid JSON: {exc}") from exc

        try:
            return output_model.model_validate(data)
        except ValidationError as exc:
            raise RuntimeError(
                f"Model response did not match {output_model.__name__}: {exc}"
            ) from exc
