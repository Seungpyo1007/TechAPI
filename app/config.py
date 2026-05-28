"""Application configuration loaded from environment (§4, appendix B)."""

from __future__ import annotations

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app import __version__


class Settings(BaseSettings):
    """Environment-driven settings. See ``.env.example`` (appendix B)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "sqlite:///./techapi.db"
    database_pool_size: int = 10

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_env: str = "development"
    api_base_url: str = "http://localhost:8000"
    api_version_prefix: str = "/v1"

    # Project metadata
    version: str = __version__
    scoring_algorithm_version: str = "1.0.0"

    # Security
    secret_key: str = "change-me"
    cors_origins: list[str] = ["http://localhost:3000", "https://techpicks.app"]

    # Logging
    log_level: str = "INFO"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, value: object) -> object:
        """Allow a comma-separated string in the env file."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()
