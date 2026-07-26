import pytest
import time
from collections.abc import Iterator

from src.psycho_navigator.config import get_settings, Settings


@pytest.fixture(autouse=True)
def execute_time():
    start = time.time()
    yield
    end = time.time()
    print(f"\nТесты выполнился за: {(end - start):.5f} сек.\n")


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        app_name="Test API",
        app_version="3.0.0",
        app_environment="test",
        debug=True,
    )
