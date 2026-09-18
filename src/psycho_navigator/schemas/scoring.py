from enum import StrEnum, IntEnum, auto

from pydantic import BaseModel


class AspectCode(IntEnum):
    first = 1
    second = 2
    third = 3


class FeatureCode(StrEnum):
    E = auto()
    A = auto()
    C = auto()
    N = auto()
    O = auto()


class Score(BaseModel):
    question_id: int
    FeatureCode: FeatureCode
    AspectCode: AspectCode
