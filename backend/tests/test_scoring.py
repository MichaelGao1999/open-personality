from pathlib import Path

import pytest

from backend.app.core.scoring import ScoringEngine
from backend.app.schemas.models import AnswerItem


@pytest.fixture
def engine():
    data_dir = str(Path(__file__).resolve().parent.parent / "data")
    return ScoringEngine(data_dir=data_dir)


@pytest.fixture
def all_3_answers() -> list[AnswerItem]:
    return [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]


@pytest.fixture
def all_1_answers() -> list[AnswerItem]:
    return [AnswerItem(item_id=f"ipip_{i:03d}", value=1) for i in range(1, 121)]


@pytest.fixture
def all_5_answers() -> list[AnswerItem]:
    return [AnswerItem(item_id=f"ipip_{i:03d}", value=5) for i in range(1, 121)]


def test_all_3_midpoint(engine, all_3_answers):
    result = engine.calculate(all_3_answers, "standard")
    assert len(result.raw_scores) == 5
    assert len(result.t_scores) == 5
    assert len(result.facet_scores) == 30
    for dim in ["O", "C", "E", "A", "N"]:
        assert dim in result.raw_scores


def test_all_1_and_all_5_symmetry(engine, all_1_answers, all_5_answers):
    result_1 = engine.calculate(all_1_answers, "standard")
    result_5 = engine.calculate(all_5_answers, "standard")
    for dim in ["O", "C", "E", "A", "N"]:
        assert result_1.raw_scores[dim] == result_5.raw_scores[dim]


def test_alternating_values(engine):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=1 if i % 2 == 0 else 5) for i in range(1, 121)]
    result = engine.calculate(answers, "standard")
    for dim in ["O", "C", "E", "A", "N"]:
        assert dim in result.raw_scores


def test_facet_scores_count(engine, all_3_answers):
    result = engine.calculate(all_3_answers, "standard")
    assert len(result.facet_scores) == 30


def test_reverse_scoring(engine):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=5) for i in range(1, 121)]
    result = engine.calculate(answers, "standard")
    assert len(result.raw_scores) == 5


def test_known_answers_consistency(engine):
    answers_a = [AnswerItem(item_id=f"ipip_{i:03d}", value=4) for i in range(1, 121)]
    answers_b = [AnswerItem(item_id=f"ipip_{i:03d}", value=4) for i in range(1, 121)]
    result_a = engine.calculate(answers_a, "standard")
    result_b = engine.calculate(answers_b, "standard")
    assert result_a.raw_scores == result_b.raw_scores


def test_invalid_item_id_ignored(engine):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]
    answers.append(AnswerItem(item_id="invalid_id", value=3))
    result = engine.calculate(answers, "standard")
    assert len(result.raw_scores) == 5


def test_item_facet_names_match_interpretations():
    """Ensure facet names in item files match interpretation keys."""
    import json

    data_dir = Path(__file__).resolve().parent.parent / "data"

    # Get facets from all item files
    for mode_key, mode_name in [("120", "standard"), ("300", "advanced"), ("_speed", "speed")]:
        for lang in ["zh", "en"]:
            items_path = data_dir / "items" / f"ipip{mode_key}_{lang}.json"
            if not items_path.exists():
                continue

            with open(items_path, "r", encoding="utf-8") as f:
                items_data = json.load(f)

            interp_path = data_dir / f"interpretations_{lang}.json"
            with open(interp_path, "r", encoding="utf-8") as f:
                interp_data = json.load(f)

            item_facets = set(item["facet"] for item in items_data["items"])
            interp_facets = set(k for k in interp_data.keys() if k not in ["O", "C", "E", "A", "N"])

            missing = item_facets - interp_facets
            assert not missing, f"Mode {mode_name} ({lang}): facets {missing} have no interpretations"
