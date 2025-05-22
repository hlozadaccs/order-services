import os

from pydantic_settings import BaseSettings

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/db"
)
DJANGO_SERVICE_URL = os.getenv("DJANGO_SERVICE_URL", "http://localhost:8000")
POD_NAME = os.getenv("POD_NAME") or open("/etc/hostname").read().strip()


class Settings(BaseSettings):
    DATABASE_URL: str = DATABASE_URL

    class Config:
        env_file = ".env"


settings = Settings()
