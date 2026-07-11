from fastapi import APIRouter, Path, HTTPException, status
from typing import Annotated

from psycho_navigator.schemas.tests import TestResponse
from psycho_navigator.data.tests import tests, Test

router = APIRouter(prefix="/tests", tags=["tests"])


@router.get("/", response_model=list[TestResponse])
async def get_tests() -> list[Test]:
    return tests


@router.get("/{test_id}", response_model=TestResponse)
async def get_test(test_id: Annotated[int, Path(ge=1)]) -> Test:
    for i in tests:
        if i["id"] == test_id:
            return i
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found.")
