"""
Application configuration using Pydantic Settings.

Loads configuration from environment variables (.env file).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str

    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # Google Gemini AI
    GEMINI_API_KEY: str

    # Rate Limiting
    MEAL_PLAN_USER_LIMIT_PER_WEEK: int = 2
    GEMINI_REQUESTS_PER_MINUTE: int = 15
    GEMINI_DAILY_LIMIT: int = 1500
    GEMINI_DAILY_ALERT_THRESHOLD: int = 1200

    # OCR Settings
    OCR_CONFIDENCE_THRESHOLD: float = 0.6
    PADDLEOCR_LANG: str = "en"

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()
