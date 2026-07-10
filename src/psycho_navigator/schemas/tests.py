from pydantic import BaseModel, Field, field_validator, ValidationInfo


class TestResponse(BaseModel):
    id: int = Field(ge=1, description="ID of the test.")
    name: str = Field(description="Name of the test.")
    description: str = Field(description="Description of the test.")

    @field_validator("name", "description")
    def validate_non_empty_string(cls, value: str, info: ValidationInfo) -> str:
        if not (normalized := value.strip()):
            raise ValueError(f"{info.field_name} can not be empty.")
        return normalized
