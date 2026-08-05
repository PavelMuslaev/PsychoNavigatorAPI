from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import TypedDict


class AnswerScaleType(TypedDict):
    value: int
    label: str


class QuestionType(TypedDict):
    id: int
    text: str


class TestResponse(BaseModel):
    id: int = Field(ge=1, description="ID of the test.")
    name: str = Field(description="Name of the test.")
    description: str = Field(description="Description of the test.")

    @field_validator("name", "description")
    @classmethod
    def validate_non_empty_string(cls, value: str, info: ValidationInfo) -> str:
        if not (normalized := value.strip()):
            raise ValueError(f"{info.field_name} can not be empty.")
        return normalized


class QuestionnaireResponse(TestResponse):
    instructions: str = Field(description="Instructions of the test.")
    answer_scale: list[AnswerScaleType] = Field(
        description="Answer scales of the test."
    )
    questions: list[QuestionType] = Field(description="Questions of the test.")

    @field_validator("instructions")
    @classmethod
    def validate_non_empty_string(cls, value: str, info: ValidationInfo) -> str:
        if not (normalized := value.strip()):
            raise ValueError(f"{info.field_name} can not be empty.")
        return normalized
