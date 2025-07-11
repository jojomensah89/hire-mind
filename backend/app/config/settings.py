from typing import List
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Board AI"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]  # Allow all origins for now

    class Config:
        case_sensitive = True
        env_file = ".env.dev", ".env.prod", ".env.example"
        env_file_encoding = 'utf-8'


settings = Settings()
