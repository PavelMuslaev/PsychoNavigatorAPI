import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from pydantic import ValidationError

from psycho_navigator.schemas.tests import QuestionnaireResponse


QuestionnaireCollection = tuple[QuestionnaireResponse, ...]


def read_questionnaire(path: Path) -> QuestionnaireResponse:
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise OSError(f"Failed to load questionnaire from {path}") from exc
    else:
        return QuestionnaireResponse.model_validate(data)


def load_questionnaires(
    dir_path: Path, *, max_workers: int = 8
) -> QuestionnaireCollection:
    paths = [
        path for path in dir_path.iterdir() if path.is_file() and path.suffix == ".json"
    ]

    if not paths:
        raise RuntimeError(f"No questionnaire JSON files found in {dir_path}")

    with ThreadPoolExecutor(max_workers) as pool:
        tests = tuple(pool.map(read_questionnaire, paths))

    return tests
