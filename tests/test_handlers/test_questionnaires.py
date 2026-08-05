import json
from json import JSONDecodeError

import pytest
from pydantic import ValidationError

from psycho_navigator.handlers.tests.questionnaires import read_questionnaire


@pytest.fixture
def make_questionnaire_payload() -> dict:
    return {
        "id": 1,
        "name": "Test",
        "description": "Description",
        "instructions": "Instructions",
        "answer_scale": [
            {"value": 1, "label": "One"},
            {"value": 2, "label": "Two"},
            {"value": 3, "label": "Three"},
            {"value": 4, "label": "Four"},
            {"value": 5, "label": "Five"},
        ],
        "questions": [{"id": 1, "text": "Question"}],
    }


def test_read_questionnaire_rejects_broken_json(tmp_path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Failed to load questionnaire") as exc_info:
        read_questionnaire(path)

    assert isinstance(exc_info.value.__cause__, JSONDecodeError)


def test_read_questionnaire_rejects_invalid_nested_data(
    tmp_path, make_questionnaire_payload
) -> None:
    payload = make_questionnaire_payload
    payload["questions"] = [{"id": 0, "text": "Question"}]
    path = tmp_path / "invalid_nested_data.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="Failed to load questionnaire") as exc_info:
        read_questionnaire(path)

    assert isinstance(exc_info.value.__cause__, ValidationError)
