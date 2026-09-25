"""Database and application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Database and application configuration."""

    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5432/fradms"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
