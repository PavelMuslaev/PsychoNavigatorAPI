from fastapi.testclient import TestClient

from src.psycho_navigator.main import create_app
from src.psycho_navigator.config import Settings, get_settings
from psycho_navigator.api.routers import get_router


class TestHealth:
    def test_get_health(self, settings) -> None:
        app = create_app(settings, get_router())
        # НЕ ХОЧУ ДЕРГАТЬ РЕАЛЬНУЮ АПИШКУ, МОЖЕТ ПАТЧИТЬ?
