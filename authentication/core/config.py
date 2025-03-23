# authentication/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Authentication Service"
    DESCRIPTION: str = "Handles user registration, login, and token verification."
    VERSION: str = "1.0.0"

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int = 30

    class Config:
        env_file = "authentication/.env"
        env_file_encoding = "utf-8"


# Create a singleton settings instance
settings = Settings()
