from fastapi.testclient import TestClient

from psycho_navigator.main import app


client = TestClient(app)


class TestHealth:
    def test_get_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "app_name": "Psycho Navigator API",
            "app_version": "0.1.0",
            "app_environment": "local",
            "debug": False,
        }
