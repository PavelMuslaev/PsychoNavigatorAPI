from psycho_navigator.schemas.results import EpiResult


class EpiScorer:
    """Form A. Answer values: 1 = yes, 2 = no."""

    def score(self, answers: dict[int, int]) -> EpiResult:
        def matches(ids, expected):
            return sum(answers[item] == expected for item in ids)

        return EpiResult(
            test_id=2,
            extraversion=matches((1, 3, 8, 10, 13, 17, 22, 25, 27, 39, 44, 46, 49, 53, 56), 1)
            + matches((5, 15, 20, 29, 32, 34, 37, 41, 51), 2),
            neuroticism=matches((2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28,
                                 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57), 1),
            control=matches((6, 24, 36), 1) + matches((12, 18, 30, 42, 48, 54), 2),
        )
