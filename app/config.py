from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_URL: str

    PROMETHEUS_HOST: str
    PROMETHEUS_PORT: int
    PROMETHEUS_URL: str

    MONOLITHIC_PROJECT_SECRET: str
    MONOLITHIC_PROJECT_ALGORITHM: str
    MONOLITHIC_PROJECT_URL: str

    POD_NAME: str = Path("/etc/hostname").read_text().strip()

    model_config = SettingsConfigDict(env_file=".env.local")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
