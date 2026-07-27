from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    app_name: str = "PsychoNavigator API"
    app_version: str = "0.1.0"
    app_environment: Literal["local", "test", "production"] = "local"
    debug: bool = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
