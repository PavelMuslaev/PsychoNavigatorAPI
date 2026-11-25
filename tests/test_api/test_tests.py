from fastapi.testclient import TestClient

from psycho_navigator.main import app
from collections.abc import Generator
from typing import Any

import pytest


SUMMARY_FIELDS = {"id", "name", "description"}
FULL_RESPONSE_FIELDS = {
    "id",
    "name",
    "description",
    "instructions",
    "answer_scale",
    "questions",
}
ANSWER_OPTION_FIELDS = {"value", "label"}
QUESTION_FIELDS = {"id", "text"}
SCORING_FIELDS = {"scoring", "scoring_key", "score", "reverse_scored", "reverse", "domain", "facet"}
EXPECTED_QUESTION_IDS = [*range(1, 28), *range(29, 62)]


@pytest.fixture(scope="session")
def get_client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


def assert_no_scoring_fields(data: Any) -> None:
    if isinstance(data, dict):
        assert SCORING_FIELDS.isdisjoint(data)
        for value in data.values():
            assert_no_scoring_fields(value)
    elif isinstance(data, list):
        for item in data:
            assert_no_scoring_fields(item)


class TestTests:
    def test_get_tests(self, get_client) -> None:
        response = get_client.get("/tests", follow_redirects=False)

        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert set(data[0]) == SUMMARY_FIELDS
        assert all("id" in item for item in data)
        assert all("name" in item for item in data)
        assert all("description" in item for item in data)
        assert_no_scoring_fields(data)

    @pytest.mark.parametrize(
        "test_id, answer, quantity_question",
        [
            (1, 200, 60),
        ],
    )
    def test_get_test_by_id(
        self, get_client, test_id: int, answer: int, quantity_question: int
    ) -> None:
        response = get_client.get(f"/tests/{test_id}")
        assert response.status_code == answer

        data = response.json()
        assert set(data) == FULL_RESPONSE_FIELDS
        assert data["id"] == test_id
        assert len(data["questions"]) == quantity_question
        assert_no_scoring_fields(data)

    def test_get_test_by_id_returns_expected_question_ids(self, get_client) -> None:
        response = get_client.get("/tests/1")

        assert response.status_code == 200

        question_ids = [question["id"] for question in response.json()["questions"]]
        assert question_ids == EXPECTED_QUESTION_IDS
        assert 28 not in question_ids
        assert 61 in question_ids
        assert 60 in question_ids

    def test_get_test_by_id_returns_answer_scale_in_order(self, get_client) -> None:
        response = get_client.get("/tests/1")

        assert response.status_code == 200

        answer_scale = response.json()["answer_scale"]
        assert [option["value"] for option in answer_scale] == [1, 2, 3, 4, 5]
        assert all(set(option) == ANSWER_OPTION_FIELDS for option in answer_scale)

    def test_get_test_by_id_returns_question_fields(self, get_client) -> None:
        response = get_client.get("/tests/1")

        assert response.status_code == 200

        questions = response.json()["questions"]
        assert all(set(question) == QUESTION_FIELDS for question in questions)

    @pytest.mark.parametrize(
        "test_id, answer",
        [
            (6, 404),
            (7, 404),
        ],
    )
    def test_get_test_returns_404_id(
        self, get_client, test_id: int, answer: int
    ) -> None:
        response = get_client.get(f"/tests/{test_id}")
        assert response.status_code == answer
        assert response.json() == {"detail": "Test not found."}

    @pytest.mark.parametrize(
        "test_id, answer",
        [
            (-1, 422),
            (0, 422),
            ("abc", 422),
        ],
    )
    def test_get_test_returns_422_id(
        self, get_client, test_id: int, answer: int
    ) -> None:
        response = get_client.get(f"/tests/{test_id}")
        assert response.status_code == answer
