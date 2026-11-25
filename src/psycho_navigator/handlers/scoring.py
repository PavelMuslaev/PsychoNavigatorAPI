from pathlib import Path

from psycho_navigator.schemas.scoring import Bfi2Key
from psycho_navigator.schemas.tests import QuestionnaireResponse


def load_bfi2_key(path: Path, questionnaires: list[QuestionnaireResponse]) -> Bfi2Key:
    try:
        key = Bfi2Key.model_validate_json(path.read_bytes())
        matches = [test for test in questionnaires if test.id == 1]
        if len(matches) != 1:
            raise ValueError("Expected exactly one BFI-2 questionnaire with ID 1")
        questions = matches[0].questions
        if len(questions) != 60 or {q.id for q in questions} != {
            entry.question_id for entry in key.items
        }:
            raise ValueError("BFI-2 question IDs and scoring key do not match")
        return key
    except (OSError, ValueError) as error:
        raise RuntimeError(f"Invalid BFI-2 configuration at {path}: {error}") from error
