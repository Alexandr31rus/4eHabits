from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    ENV: str
    LOG_LEVEL: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=ENV_FILE, extra="ignore", env_file_encoding="utf-8"
    )


settings = Settings()
