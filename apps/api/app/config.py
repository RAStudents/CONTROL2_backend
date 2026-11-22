from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "CONTROL API"
    API_V1_STR: str = "/api"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/control_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    MEDIA_DIR: str = "/app/media"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
