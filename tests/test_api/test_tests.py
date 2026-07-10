from fastapi.testclient import TestClient

from psycho_navigator.main import app

import pytest

client = TestClient(app)


class TestTests:
    def test_get_tests(self):
        response = client.get("/tests/")

        assert response.status_code == 200

        data = response.json()
        assert len(data) == 5
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)
        assert all("description" in item for item in data)

    @pytest.mark.parametrize(
        "test_id, answer",
        [
            (1, 200),
            (2, 200),
            (3, 200),
            (4, 200),
            (5, 200),
        ],
    )
    def test_get_test_by_id(self, test_id, answer):
        response = client.get(f"/tests/{test_id}")
        assert response.status_code == answer
        assert response.json()["id"] == test_id

    @pytest.mark.parametrize(
        "test_id, answer",
        [
            (6, 404),
            (7, 404),
        ],
    )
    def test_get_test_returns_404_id(self, test_id, answer):
        response = client.get(f"/tests/{test_id}")
        assert response.status_code == answer

    @pytest.mark.parametrize(
        "test_id, answer",
        [
            (-1, 422),
            (0, 422),
        ],
    )
    def test_get_test_returns_422_id(self, test_id, answer):
        response = client.get(f"/tests/{test_id}")
        assert response.status_code == answer
