import pytest
from pydantic import ValidationError

from psycho_navigator.config import get_settings


def test_get_settings_read_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_NAME", "Test API")
    monkeypatch.setenv("APP_VERSION", "2.0.0")
    monkeypatch.setenv("APP_ENVIRONMENT", "test")
    monkeypatch.setenv("DEBUG", "true")

    settings = get_settings()

    assert settings.app_name == "Test API"
    assert settings.app_version == "2.0.0"
    assert settings.app_environment == "test"
    assert settings.debug is True


def test_get_settings_rejects_unknown_environment(
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv("APP_ENVIRONMENT", "baka buka")
    with pytest.raises(ValidationError):
        get_settings()
