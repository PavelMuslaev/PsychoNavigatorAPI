from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from psycho_navigator.api.routers import get_router
from psycho_navigator.config import Settings
from psycho_navigator.main import create_app


def test_history_lifecycle(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "history.db"))
    monkeypatch.setenv("HISTORY_TOKEN", "service-test")
    command.upgrade(Config("alembic.ini"), "head")
    headers = {"Authorization": "Bearer service-test"}
    path = "/users/1/attempts"
    attempt = "/" + str(uuid4())
    payload = {
        "answers": [{"question_id": i, "value": 3} for i in range(1, 62) if i != 28]
    }

    def client():
        return TestClient(create_app(Settings(), get_router()))

    with client() as api:
        assert api.post(path + attempt, json=payload).status_code == 401
        assert api.get(path).status_code == 401
        assert (
            api.post(path + attempt, json={"answers": []}, headers=headers).status_code
            == 422
        )
        assert api.get(path, headers=headers).json() == []
        expected = api.post("/tests/1/results", json=payload).json()
        assert api.get(path, headers=headers).json() == []

        def save(_):
            response = api.post(path + attempt, json=payload, headers=headers)
            assert response.status_code == 200
            return response.json()

        with ThreadPoolExecutor(2) as pool:
            first, retry = pool.map(save, range(2))
        assert first == retry
        assert first["profile"] == expected

    with client() as api:
        assert api.get(path + attempt, headers=headers).json() == first
        assert len(api.get(path, headers=headers).json()) == 1
        assert api.get("/users/2/attempts", headers=headers).json() == []
        assert (
            api.get("/users/2/attempts" + attempt, headers=headers).status_code == 404
        )
        second = api.post(
            path + "/" + str(uuid4()), json=payload, headers=headers
        ).json()
        assert (
            api.get(path + "?limit=1", headers=headers).json()[0]["attempt_id"]
            == second["attempt_id"]
        )
        assert api.get(path + "?limit=51", headers=headers).status_code == 422
