import os
from functools import lru_cache

# isort: skip_file
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    app_env: str
    secret_key: str
    database_url: str | None = None

    postgres_db: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('APP_ENV', 'dev')}", case_sensitive=False
    )
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()


class DBConfig:
    if settings.app_env == "dev":
        DATABASE_URL = settings.database_url
        engine = create_async_engine(DATABASE_URL, echo=True)
        async_sessionmaker_ = async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )
    else:
        DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@localhost:5432/{settings.postgres_db}"  # noqa E501s
        engine = create_async_engine(DATABASE_URL, echo=False)
        async_sessionmaker_ = async_sessionmaker(
            bind=engine, expire_on_commit=False, class_=AsyncSession
        )


class Base(DeclarativeBase):
    pass
