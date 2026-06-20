from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # `.env` is used when running from `backend/`; `backend/.env` supports running from repo root.
    model_config = SettingsConfigDict(env_file=(".env", "backend/.env"), env_file_encoding="utf-8", case_sensitive=True)

    APP_NAME: str = "LLM RAG Chatbot API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app.db"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | list[str] = Field(default_factory=list)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
