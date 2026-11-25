from pydantic import BaseModel, ConfigDict, Field

from psycho_navigator.schemas.scoring import DomainCode, FacetCode


class AnswerSubmission(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    question_id: int = Field(ge=1)
    value: int


class QuestionnaireResultRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answers: list[AnswerSubmission]


class FacetScore(BaseModel):
    code: FacetCode
    name: str
    score: float


class DomainScore(BaseModel):
    code: DomainCode
    name: str
    score: float
    facets: list[FacetScore]


class QuestionnaireResultResponse(BaseModel):
    test_id: int
    domains: list[DomainScore]
