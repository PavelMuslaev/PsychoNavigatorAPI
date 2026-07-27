import pytest
import time
from collections.abc import Iterator

from psycho_navigator.config import get_settings, Settings


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
def settings(
    monkeypatch: pytest.MonkeyPatch,
) -> Settings:
    monkeypatch.setenv("APP_NAME", "Test API")
    monkeypatch.setenv("APP_VERSION", "3.0.0")
    monkeypatch.setenv("APP_ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "True")

    return Settings()
