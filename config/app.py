import os
from enum import Enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    NOTSET = "NOTSET"


class Settings(BaseSettings):
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = os.getenv("PORT", "8000")
    workers_count: int = os.getenv("WORKERS", "4")
    reload: bool = os.getenv("RELOAD", True)

    environment: str = os.getenv("ENVIRONMENT", "dev")

    log_level: LogLevel = os.getenv("LOG_LEVEL", LogLevel.INFO)

    user_secret: str = os.getenv("USER_SECRET", "")

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = os.getenv("DB_PORT", 5432)
    db_user: str = os.getenv("DB_USER", "dev")
    db_pass: str = os.getenv("DB_PASS", "dev")
    db_name: str = os.getenv("DB_NAME", "dev")

    db_echo: bool = os.getenv("DB_ECHO", False)

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_name}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
