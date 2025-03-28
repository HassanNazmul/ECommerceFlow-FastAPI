# core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Product Service"
    DESCRIPTION: str = "Handles the creation, updating, and deletion of products."
    VERSION: str = "1.0.0"

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int = 30

    class Config:
        env_file = "product/.env"
        env_file_encoding = "utf-8"


# Create an instance of the Settings class
settings = Settings()
