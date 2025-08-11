import os
from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Port to listen on
    # Default to 3500
    port: str = os.getenv("PORT", "3500")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()