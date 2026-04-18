from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..config import load_settings
from .routes import build_router


def create_app() -> FastAPI:
    settings = load_settings()
    app = FastAPI(title="Startup Factory API", version="3.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(build_router(), prefix="/api/v1")
    return app


app = create_app()
