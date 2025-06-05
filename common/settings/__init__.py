from functools import lru_cache

from .settings import Settings

@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Create a global settings instance
settings = get_settings()

__all__ = ["settings", "get_settings"] 