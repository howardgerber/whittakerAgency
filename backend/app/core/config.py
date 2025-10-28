from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours

    # Email (Brevo)
    BREVO_API_KEY: str = "stub"
    BREVO_SENDER_EMAIL: str = "noreply@whittakeragency.com"
    BREVO_ADMIN_EMAIL: str = "admin@whittakeragency.com"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3003,http://localhost:8082"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
