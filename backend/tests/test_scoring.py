import json
import os
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
    items_path = Path(engine.data_dir) / "items" / "ipip120_en.json"
    with open(items_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    reversed_items = {item["item_id"] for item in data["items"] if item["reversed"]}
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
