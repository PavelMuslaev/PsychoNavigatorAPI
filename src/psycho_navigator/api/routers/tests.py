from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Path as PathParam,
    Request,
)

from psycho_navigator.handlers.epi import EpiScorer
from psycho_navigator.handlers.results import QuestionnaireScorer, validate_answers
from psycho_navigator.schemas.results import EpiResult, QuestionnaireResultRequest, QuestionnaireResultResponse
from psycho_navigator.handlers.tests.questionnaires import QuestionnaireCollection
from psycho_navigator.schemas.tests import TestResponse, QuestionnaireResponse


router = APIRouter(prefix="/tests", tags=["tests"])


async def get_questionnaires(
    request: Request,
) -> QuestionnaireCollection:
    return request.app.state.questionnaires


QuestionnaireDepends = Annotated[QuestionnaireCollection, Depends(get_questionnaires)]


@router.get("", response_model=list[TestResponse])
async def get_tests(questionnaires: QuestionnaireDepends) -> list[TestResponse]:
    return questionnaires


@router.get("/{test_id}", response_model=QuestionnaireResponse, response_model_exclude_none=True)
async def get_test(
    test_id: Annotated[int, PathParam(ge=1)],
    questionnaires: QuestionnaireDepends,
) -> QuestionnaireResponse:
    for test in questionnaires:
        if test.id == test_id:
            return test

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found.")


@router.post("/{test_id}/results", response_model=QuestionnaireResultResponse | EpiResult)
async def calculate_result(
    test_id: Annotated[int, PathParam(ge=1)],
    submission: QuestionnaireResultRequest,
    questionnaires: QuestionnaireDepends,
    request: Request,
) -> QuestionnaireResultResponse | EpiResult:
    test = await get_test(test_id, questionnaires)
    scorers: dict[int, QuestionnaireScorer] = request.app.state.scorers
    if test_id != 2 and test_id not in scorers:
        raise HTTPException(status_code=501, detail="Scoring unavailable for this test")
    try:
        answers = validate_answers(test, submission.answers)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=error.args[0]) from error
    if test_id == 2:
        return EpiScorer().score(answers)
    return QuestionnaireResultResponse(test_id=test_id, domains=scorers[test_id].score(answers))
