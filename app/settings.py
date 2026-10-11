"""Paramètres de configuration de l'application."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Paramètres globaux de l'application."""

    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite:///./talent_engine.db"
    )
    app_title: str = os.getenv("APP_TITLE", "Talent Engine")
    debug: bool = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"}


settings = Settings()
