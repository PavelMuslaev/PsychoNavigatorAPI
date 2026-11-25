from collections import Counter, defaultdict
from statistics import mean
from typing import Protocol

from psycho_navigator.schemas.results import AnswerSubmission, DomainScore, FacetScore
from psycho_navigator.schemas.scoring import Bfi2Key, DomainCode, FacetCode
from psycho_navigator.schemas.tests import QuestionnaireResponse


NAMES = {
    DomainCode.E: ("Экстраверсия", "Общительность", "Настойчивость", "Энергичность"),
    DomainCode.A: ("Доброжелательность", "Сочувствие", "Уважительность", "Доверие"),
    DomainCode.C: ("Добросовестность", "Организованность", "Продуктивность", "Ответственность"),
    DomainCode.N: ("Негативная эмоциональность", "Тревожность", "Депрессивность", "Эмоциональная изменчивость"),
    DomainCode.O: ("Открытость опыту", "Эстетичность", "Любознательность", "Творческое воображение"),
}


def validate_answers(test: QuestionnaireResponse, answers: list[AnswerSubmission]) -> dict[int, int]:
    counts = Counter(answer.question_id for answer in answers)
    expected = {question.id for question in test.questions}
    scale = {option.value for option in test.answer_scale}
    problems = {
        "duplicate": sorted(i for i, count in counts.items() if count > 1),
        "missing": sorted(expected - counts.keys()),
        "unknown": sorted(counts.keys() - expected),
        "outside_scale": sorted({a.question_id for a in answers if a.value not in scale}),
    }
    if errors := {name: ids for name, ids in problems.items() if ids}:
        raise ValueError(errors)
    return {answer.question_id: answer.value for answer in answers}


class QuestionnaireScorer(Protocol):
    def score(self, answers: dict[int, int]) -> list[DomainScore]: ...


class Bfi2Scorer:
    def __init__(self, key: Bfi2Key):
        self.key = key

    def score(self, answers: dict[int, int]) -> list[DomainScore]:
        values: dict[FacetCode, list[int]] = defaultdict(list)
        for entry in self.key.items:
            value = answers[entry.question_id]
            values[entry.facet].append(6 - value if entry.reverse else value)

        domains = []
        for domain, (name, *facet_names) in NAMES.items():
            facets = []
            domain_values = []
            for index, facet_name in enumerate(facet_names, start=1):
                code = FacetCode(f"{domain}{index}")
                domain_values.extend(values[code])
                facets.append(FacetScore(code=code, name=facet_name, score=round(mean(values[code]), 2)))
            domains.append(DomainScore(code=domain, name=name, score=round(mean(domain_values), 2), facets=facets))
        return domains
