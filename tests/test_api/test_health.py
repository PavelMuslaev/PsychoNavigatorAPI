from fastapi.testclient import TestClient

from psycho_navigator.main import app

client = TestClient(app)


class TestHealth:
    def test_get_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "version": "0.1.0",
            "environment": "local"
        }
