import pytest

from psycho_navigator.handlers.epi import EpiScorer


@pytest.mark.parametrize("yes,no,expected", [(1, 2, (24, 24, 9)), (2, 1, (0, 0, 0))])
def test_epi_extremes(yes, no, expected):
    reverse_items = {5, 12, 15, 18, 20, 29, 30, 32, 34, 37, 41, 42, 48, 51, 54}
    result = EpiScorer().score({i: no if i in reverse_items else yes for i in range(1, 58)})
    assert (result.extraversion, result.neuroticism, result.control) == expected
