from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Board AI"
    API_V1_STR: str = "/api/v1"
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding='utf-8'
    )

    # Database settings
    DATABASE_URL: str

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]

    # Clerk settings
    CLERK_SECRET_KEY: str
    CLERK_PUBLISHABLE_KEY: str
    CLERK_WEBHOOK_SECRET: str
    CLERK_AUTHORIZED_PARTIES: List[str] = ["http://localhost:3000"]

settings = Settings()