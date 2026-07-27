from fastapi.testclient import TestClient

from psycho_navigator.main import create_app
from psycho_navigator.api.routers import get_router


class TestHealth:
    def test_get_health(self, settings) -> None:
        app = create_app(settings, get_router())

        with TestClient(app) as client:
            response = client.get("/health", follow_redirects=False)

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "version": "3.0.0",
            "environment": "test",
        }
