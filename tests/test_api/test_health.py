from fastapi.testclient import TestClient

from psycho_navigator.main import create_app
from psycho_navigator.api.routers import get_router
from psycho_navigator.config import get_settings, Settings


class TestHealth:
    def test_get_health(self, settings: Settings) -> None:
        app = create_app(settings, get_router())
        app.dependency_overrides[get_settings] = lambda: settings

        with TestClient(app) as client:
            response = client.get("/health", follow_redirects=False)

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "version": "3.0.0",
            "environment": "test",
        }
