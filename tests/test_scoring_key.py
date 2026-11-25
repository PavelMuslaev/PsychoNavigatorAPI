import json
from collections import Counter

import pytest

from psycho_navigator.handlers.scoring import load_bfi2_key
from psycho_navigator.handlers.tests.questionnaires import load_questionnaires


def test_alternative_key(settings):
    tests = load_questionnaires(settings.path_dir_tests)
    key = load_bfi2_key(settings.scoring_key_path, tests)
    by_id = {entry.question_id: entry for entry in key.items}
    assert set(by_id) == set(range(1, 62)) - {28}
    assert by_id[60].facet == "O3" and not by_id[60].reverse
    assert by_id[61].facet == "C3" and by_id[61].reverse
    assert list(Counter(e.domain for e in key.items).values()) == [12] * 5
    assert list(Counter(e.facet for e in key.items).values()) == [4] * 15


@pytest.mark.parametrize("patch", [
    {"question_id": 2}, {"question_id": 28}, {"domain": "X"},
    {"facet": "Z3"}, {"facet": "A1"}, {"facet": "E2"}, {"reverse": 0},
])
def test_invalid_key(settings, tmp_path, patch):
    payload = json.loads(settings.scoring_key_path.read_bytes())
    payload["items"][0].update(patch)
    path = tmp_path / "key.json"
    path.write_text(json.dumps(payload))
    with pytest.raises(RuntimeError, match="Invalid BFI-2 configuration"):
        load_bfi2_key(path, load_questionnaires(settings.path_dir_tests))
