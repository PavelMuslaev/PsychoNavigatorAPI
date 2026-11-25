import pytest
from fastapi.testclient import TestClient

from psycho_navigator.main import app
from psycho_navigator.handlers.results import Bfi2Scorer


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def answers(value=3):
    return [{"question_id": i, "value": value} for i in range(1, 62) if i != 28]


@pytest.mark.parametrize("value", [1, 5])
def test_balanced_key(client, value):
    scores = Bfi2Scorer(app.state.bfi2_key).score({a["question_id"]: value for a in answers()})
    assert [d.score for d in scores] == [3] * 5
    assert all([f.score for f in d.facets] == [3] * 3 for d in scores)


def test_mixed_result(client):
    payload = answers()
    payload[0]["value"] = 5  # direct E1: +2
    payload[15]["value"] = 2  # reverse E1: +1
    for order in [payload, payload[::-1]]:
        response = client.post("/tests/1/results", json={"answers": order})
        assert response.status_code == 200
        profile = response.json()
        assert set(profile) == {"test_id", "domains"}
        assert [d["code"] for d in profile["domains"]] == list("EACNO")
        first = profile["domains"][0]
        assert first["score"] == 3.25
        assert [f["score"] for f in first["facets"]] == [3.75, 3, 3]
        for d in profile["domains"]:
            assert set(d) == {"code", "name", "score", "facets"}
            assert len(d["facets"]) == 3
            assert all(set(f) == {"code", "name", "score"} for f in d["facets"])


@pytest.mark.parametrize("change", [
    lambda data: data.pop(),
    lambda data: data.append(data[0]),
    lambda data: data[0].update(question_id=28),
    lambda data: data[0].update(value=6),
    lambda data: data[0].update(value=True),
])
def test_reject_invalid_answers(client, change):
    data = answers()
    change(data)
    assert client.post("/tests/1/results", json={"answers": data}).status_code == 422


@pytest.mark.parametrize(("path", "status"), [("0", 422), ("abc", 422), ("2", 404)])
def test_unknown_test(client, path, status):
    assert client.post(f"/tests/{path}/results", json={"answers": answers()}).status_code == status


def test_missing_scorer(client, monkeypatch):
    monkeypatch.delitem(app.state.scorers, 1)
    assert client.post("/tests/1/results", json={"answers": answers()}).status_code == 501
