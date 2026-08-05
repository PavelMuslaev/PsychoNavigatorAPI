from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Final
from functools import lru_cache
from pathlib import Path


PACKAGE_DIR: Final = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    app_name: str = "PsychoNavigator API"
    app_version: str = "0.1.0"
    app_environment: Literal["local", "test", "production"] = "local"
    debug: bool = False
    path_dir_tests: Path = PACKAGE_DIR / "data" / "tests"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
