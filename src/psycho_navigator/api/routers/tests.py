from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Path as PathParam,
    Request,
)

from psycho_navigator.handlers.tests.questionnaires import QuestionnaireCollection
from psycho_navigator.schemas.tests import TestResponse, QuestionnaireResponse


router = APIRouter(prefix="/tests", tags=["tests"])


async def get_questionnaires(
    request: Request,
) -> QuestionnaireCollection:
    return request.app.state.questionnaires


QuestionnaireDepends = Annotated[QuestionnaireCollection, Depends(get_questionnaires)]


@router.get("", response_model=tuple[TestResponse, ...])
async def get_tests(questionnaires: QuestionnaireDepends) -> tuple[TestResponse, ...]:
    return questionnaires


@router.get("/{test_id}", response_model=QuestionnaireResponse)
async def get_test(
    test_id: Annotated[int, PathParam(ge=1)],
    questionnaires: QuestionnaireDepends,
) -> QuestionnaireResponse:
    for test in questionnaires:
        if test.id == test_id:
            return test

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found.")
