from pathlib import Path

import pytest

from backend.app.core.mbti import MBTIInference
from backend.app.core.scoring import ScoringEngine
from backend.app.schemas.models import AnswerItem, ScoringResult


@pytest.fixture
def data_dir():
    return str(Path(__file__).resolve().parent.parent / "data")


@pytest.fixture
def inference(data_dir):
    return MBTIInference(data_dir=data_dir)


@pytest.fixture
def engine(data_dir):
    return ScoringEngine(data_dir=data_dir)


def test_mbti_dimensions_count(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 50, "E": 50, "A": 50, "N": 50}, t_scores={}, facet_scores={})
    result = inference.infer(scores)
    assert len(result.dimensions) == 4
    assert result.type_code in ["ENFP", "ENFJ", "ENTP", "ENTJ", "ESFP", "ESFJ", "ESTP", "ESTJ",
                                 "INFP", "INFJ", "INTP", "INTJ", "ISFP", "ISFJ", "ISTP", "ISTJ"]


def test_high_E_extraversion(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 50, "E": 80, "A": 50, "N": 30}, t_scores={"E": 65, "N": 35}, facet_scores={})
    result = inference.infer(scores)
    ei_dim = [d for d in result.dimensions if d.label_a == "E"][0]
    assert ei_dim.prob_a > 0.5


def test_low_E_introversion(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 50, "E": 20, "A": 50, "N": 50}, t_scores={"E": 35}, facet_scores={})
    result = inference.infer(scores)
    ei_dim = [d for d in result.dimensions if d.label_a == "E"][0]
    assert ei_dim.prob_b > 0.5


def test_high_O_intuition(inference):
    scores = ScoringResult(raw_scores={"O": 80, "C": 50, "E": 50, "A": 50, "N": 50}, t_scores={"O": 65}, facet_scores={})
    result = inference.infer(scores)
    sn_dim = [d for d in result.dimensions if d.label_a == "S"][0]
    assert sn_dim.prob_b > 0.5


def test_high_A_feeling(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 50, "E": 50, "A": 80, "N": 50}, t_scores={"A": 65}, facet_scores={})
    result = inference.infer(scores)
    tf_dim = [d for d in result.dimensions if d.label_a == "T"][0]
    assert tf_dim.prob_b > 0.5


def test_high_C_conscientiousness(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 80, "E": 50, "A": 50, "N": 50}, t_scores={"C": 65}, facet_scores={})
    result = inference.infer(scores)
    jp_dim = [d for d in result.dimensions if d.label_a == "J"][0]
    assert jp_dim.prob_a > 0.5


def test_probability_sum_to_one(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 50, "E": 50, "A": 50, "N": 50}, t_scores={}, facet_scores={})
    result = inference.infer(scores)
    for dim in result.dimensions:
        assert abs(dim.prob_a + dim.prob_b - 1.0) < 0.001


def test_confidence_range(inference):
    scores = ScoringResult(raw_scores={"O": 50, "C": 50, "E": 50, "A": 50, "N": 50}, t_scores={}, facet_scores={})
    result = inference.infer(scores)
    assert 0 <= result.confidence <= 1
