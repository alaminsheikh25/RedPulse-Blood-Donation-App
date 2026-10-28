from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "RedPulse Blood Donation Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = Field(
        default="sqlite+aiosqlite:///./redpulse.db",
        description="SQLAlchemy async database URL",
    )
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "change-me-in-production-use-strong-secret"
    access_token_expire_minutes: int = 60 * 24
    refresh_token_expire_days: int = 30
    algorithm: str = "HS256"

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    default_search_radius_km: float = 25.0
    max_search_radius_km: float = 100.0
    min_donor_age: int = 18
    max_donor_age: int = 65
    min_donor_weight_kg: float = 50.0
    min_hemoglobin_g_dl: float = 12.5
    min_donation_interval_days: int = 56
    platelet_interval_days: int = 7
    plasma_interval_days: int = 28

    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: str = "noreply@redpulse.org"

    firebase_credentials_path: Optional[str] = None

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
