from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@127.0.0.1:5432/db"

    class Config:
        env_file = ".env"


settings = Settings()
