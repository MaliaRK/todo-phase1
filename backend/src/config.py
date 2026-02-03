from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # API settings
    app_env: str = os.getenv("APP_ENV", "development")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000")) if os.getenv("PORT", "8000").isdigit() else 8000

    # Authentication settings
    secret_key: str = os.getenv("SECRET_KEY", "your-default-secret-key")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")) if os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30").isdigit() else 30

    # AI/LLM settings
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Better Auth settings
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "")

    # Additional settings
    debug: str = os.getenv("DEBUG", "false")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields that are not defined

# Create a single instance of settings
settings = Settings()

def get_settings() -> Settings:
    """
    Dependency to get application settings.

    Returns:
        Settings instance with loaded configuration
    """
    return settings