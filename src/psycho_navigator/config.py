from pydantic_settings import BaseSettings
from typing import LiteralString, Literal
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Psycho Navigator API"
    app_version: str = "0.1.0"
    app_environment: Literal["local", "test", "production"] = "local"
    debug: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
