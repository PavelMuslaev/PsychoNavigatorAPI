import pytest

from psycho_navigator.handlers.epi import EpiScorer


@pytest.mark.parametrize("yes,no,expected", [(1, 2, (24, 24, 9)), (2, 1, (0, 0, 0))])
def test_epi_extremes(yes, no, expected):
    reverse_items = {5, 12, 15, 18, 20, 29, 30, 32, 34, 37, 41, 42, 48, 51, 54}
    result = EpiScorer().score({i: no if i in reverse_items else yes for i in range(1, 58)})
    assert (result.extraversion, result.neuroticism, result.control) == expected


def test_epi_api():
    from fastapi.testclient import TestClient
    from psycho_navigator.main import app

    with TestClient(app) as client:
        questions = client.get("/tests/2").json()["questions"]
        assert [q["id"] for q in questions] == list(range(1, 58))
        assert questions[31]["answer_scale"] == [
            {"value": 1, "label": "Найти в книге"}, {"value": 2, "label": "Спросить у друзей"}
        ]
        answers = [{"question_id": q["id"], "value": 1} for q in questions]

        def submit(items):
            return client.post("/tests/2/results", json={"answers": items})

        assert submit(answers).json() == dict(test_id=2, extraversion=15, neuroticism=24, control=3)
        answers[31]["value"] = 2
        assert submit(answers).json()["extraversion"] == 16
        for invalid in [answers[:-1], answers + [answers[0]], [*answers[:-1], dict(question_id=57, value=3)]]:
            assert submit(invalid).status_code == 422
