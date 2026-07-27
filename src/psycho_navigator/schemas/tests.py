from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import TypedDict


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


class Test(TypedDict):
    """
    :param id: ID of the test.
    :param name: Name of the test.
    :param description: Description of the test.
    """

    id: int
    name: str
    description: str
