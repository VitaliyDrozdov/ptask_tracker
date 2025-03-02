import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    secret_key: str
    database_url: str


def get_settings():
    env = os.getenv("APP_ENV", "dev")
    env_file = f"{env}.env"
    return Settings(_env_file=env_file)


settings = get_settings()
