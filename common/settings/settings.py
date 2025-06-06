from functools import lru_cache
from typing import Any, Dict

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project settings
    PROJECT_NAME: str = "Task Tracker"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL settings
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "taskdb"
    DATABASE_URI: PostgresDsn | None = None

    # Task Tracker Service settings
    TASK_TRACKER_PORT: int = 8001
    TASK_TRACKER_INTERNAL_PORT: int = 8000

    @field_validator("DATABASE_URI", mode='before')
    @classmethod
    def build_db_connection(cls, v: str | None, values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()