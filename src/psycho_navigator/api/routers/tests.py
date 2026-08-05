from functools import lru_cache
from fastapi import APIRouter, Depends, HTTPException, status, Path as PathParam
from pathlib import Path
import json
from typing import Annotated
from concurrent.futures import ThreadPoolExecutor

from psycho_navigator.schemas.tests import TestResponse, QuestionnaireResponse
from psycho_navigator.config import Settings, get_settings


router = APIRouter(prefix="/tests", tags=["tests"])
SettingsDepends = Annotated[Settings, Depends(get_settings)]

@lru_cache
def read_test_file(path: Path) -> QuestionnaireResponse:
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except OSError as exc:
        raise OSError(exc) from exc

    return QuestionnaireResponse.model_validate(data)


@lru_cache
def get_tests_from_dir(dir_path: Path, *, max_workers: int = 8) -> list[QuestionnaireResponse]:
    files = [
        path for path in dir_path.iterdir() if path.is_file() and path.suffix == ".json"
    ]

    with ThreadPoolExecutor(max_workers) as pool:
        tests = list(pool.map(read_test_file, files))

    return tests


@router.get("", response_model=list[TestResponse])
async def get_tests(
    settings: SettingsDepends,
) -> list[TestResponse]:
    return get_tests_from_dir(settings.path_dir_tests)


@router.get("/{test_id}", response_model=QuestionnaireResponse)
async def get_test(
    settings: SettingsDepends, test_id: Annotated[int, PathParam(ge=1)]
) -> QuestionnaireResponse:
    tests = get_tests_from_dir(settings.path_dir_tests)
    for test in tests:
        if test.id == test_id:
            return QuestionnaireResponse.model_validate(test)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found.")
