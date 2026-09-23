"""Application configuration.

All settings are read from environment variables (or a local .env file)
via pydantic-settings. Never hard-code secrets in the source code.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Application
    APP_NAME: str = "David Musumali Personal API"
    ENVIRONMENT: str = "development"  # development | production

    # Security / JWT
    SECRET_KEY: str = "change-me-to-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # First admin account (created automatically on startup)
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "ChangeMe-Admin-2026"
    ADMIN_EMAIL: str = "dmusumali01@gmail.com"

    # Database (SQLite now, PostgreSQL-compatible URL later)
    DATABASE_URL: str = "sqlite:///./data/personal_api.db"

    # CORS — comma-separated list of allowed frontend origins
    CORS_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500,http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is parsed only once per process."""
    return Settings()


settings = get_settings()
