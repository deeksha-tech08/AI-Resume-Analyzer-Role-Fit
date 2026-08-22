from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    MONGODB_URI: str
    JWT_SECRET: str
    OPENAI_API_KEY: str
    GEMINI_API_KEY: str
    FRONTEND_URL: str = 'http://localhost:5173'
    ENVIRONMENT: str = 'development'
    LOG_LEVEL: str = 'DEBUG'
    JWT_EXPIRY_DAYS: int = 7
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    UPLOAD_DIR: str = 'uploads'

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
