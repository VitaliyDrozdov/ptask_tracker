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
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_SECRET_KEY: str = ""
    GOOGLE_REDIRECT_URI: str = ""
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"
    YANDEX_CLIENT_ID: str = ""
    YANDEX_SECRET_KEY: str = ""
    YANDEX_REDIRECT_URI: str = ""
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"

    @property
    def google_redirect_url(self):
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"  # noqa

    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"  # noqa


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
