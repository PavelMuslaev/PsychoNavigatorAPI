from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field, model_validator, ConfigDict


class FacetCode(StrEnum):
    E1 = "E1"
    E2 = "E2"
    E3 = "E3"

    A1 = "A1"
    A2 = "A2"
    A3 = "A3"

    C1 = "C1"
    C2 = "C2"
    C3 = "C3"

    N1 = "N1"
    N2 = "N2"
    N3 = "N3"

    O1 = "O1"
    O2 = "O2"
    O3 = "O3"


class DomainCode(StrEnum):
    E = "E"
    A = "A"
    C = "C"
    N = "N"
    OPENNESS = "O"


class ScoringKeyEntry(BaseModel):
    question_id: int = Field(ge=1, strict=True)
    domain: DomainCode
    facet: FacetCode
    reverse: bool = Field(strict=True)

    @model_validator(mode="after")
    def validate_facet_domain(self) -> Self:
        if not self.facet.value.startswith(self.domain.value):
            raise ValueError(
                f"Facet {self.facet.value} does not belong "
                f"to domain {self.domain.value}"
            )

        return self


class Bfi2Key(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[ScoringKeyEntry] = Field(
        min_length=60,
        max_length=60,
    )

    @model_validator(mode="after")
    def validate_structure(self) -> Self:
        from collections import Counter

        ids = [entry.question_id for entry in self.items]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate question IDs in BFI-2 key")
        facets = Counter(entry.facet for entry in self.items)
        if any(facets[code] != 4 for code in FacetCode):
            raise ValueError("Each BFI-2 facet must contain four items")
        return self
