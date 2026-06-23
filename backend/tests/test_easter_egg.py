from pathlib import Path

import pytest

from backend.app.core.easter_egg import EasterEggEngine
from backend.app.schemas.models import MBTIDimension, MBTIResult, ScoringResult


def _make_scoring(t_scores: dict | None = None) -> ScoringResult:
    base: dict[str, float] = {"O": 50.0, "C": 50.0, "E": 50.0, "A": 50.0, "N": 50.0}
    if t_scores:
        base.update({k: float(v) for k, v in t_scores.items()})
    return ScoringResult(raw_scores=base, t_scores=base, facet_scores={})


def _make_mbti(type_code: str = "INTJ", confidence: float = 0.7) -> MBTIResult:
    return MBTIResult(
        type_code=type_code,
        confidence=confidence,
        dimensions=[
            MBTIDimension(label_a="E", label_b="I", prob_a=0.3, prob_b=0.7),
            MBTIDimension(label_a="S", label_b="N", prob_a=0.4, prob_b=0.6),
            MBTIDimension(label_a="T", label_b="F", prob_a=0.6, prob_b=0.4),
            MBTIDimension(label_a="J", label_b="P", prob_a=0.7, prob_b=0.3),
        ],
    )


@pytest.fixture
def engine():
    data_dir = str(Path(__file__).resolve().parent.parent / "data")
    return EasterEggEngine(data_dir=data_dir)


def test_trigger_rate_speed(engine):
    results = []
    engine._eggs = None
    for _ in range(1000):
        engine._eggs = None
        results.append(engine.trigger(lang="en", seed=str(_), mode="speed"))
    triggered = [r for r in results if r is not None]
    rate = len(triggered) / 1000
    assert 0.05 <= rate <= 0.15, f"speed trigger rate {rate} outside 5-15%"


def test_force_always_triggers(engine):
    engine._eggs = None
    for seed in range(100):
        engine._eggs = None
        result = engine.trigger(lang="zh", seed=str(seed), force=True)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0


def test_trigger_returns_string(engine):
    engine._eggs = None
    result = engine.trigger(lang="zh", seed="test_trigger")
    if result is not None:
        assert isinstance(result, str)
        assert len(result) > 0


def test_not_triggered_returns_none(engine):
    engine._eggs = None
    results = []
    for attempt in range(200):
        engine._eggs = None
        r = engine.trigger(lang="zh", seed=f"none_seed_{attempt}")
        results.append(r)
    has_none = any(r is None for r in results)
    has_string = any(r is not None for r in results)
    assert has_none
    assert has_string


def test_zh_and_en_both_available(engine):
    engine._eggs = None
    zh_results = set()
    en_results = set()
    for i in range(500):
        engine._eggs = None
        r_zh = engine.trigger(lang="zh", seed=f"lang_{i}")
        if r_zh:
            zh_results.add(r_zh)
        engine._eggs = None
        r_en = engine.trigger(lang="en", seed=f"lang_{i}")
        if r_en:
            en_results.add(r_en)
    assert len(zh_results) > 0
    assert len(en_results) > 0


def test_all_eggs_have_content(engine):
    eggs_data = engine._load_eggs()
    for egg in eggs_data.get("eggs", []):
        assert egg.get("zh") and len(egg["zh"]) > 0
        assert egg.get("en") and len(egg["en"]) > 0
        assert "condition" in egg
    for egg in eggs_data.get("medium", []):
        assert egg.get("zh") and len(egg["zh"]) > 0
        assert egg.get("en") and len(egg["en"]) > 0
        assert "condition" in egg


def test_trigger_rate_config(engine):
    eggs_data = engine._load_eggs()
    assert eggs_data["trigger_rate"] == 0.1


def test_conditional_highest_domain(engine):
    scoring = _make_scoring(t_scores={"O": 70, "C": 50, "E": 45, "A": 55, "N": 40})
    mbti = _make_mbti()
    assert engine._match_condition({"highest_domain": "O"}, scoring, mbti, "standard")
    assert not engine._match_condition({"highest_domain": "C"}, scoring, mbti, "standard")


def test_conditional_lowest_domain(engine):
    scoring = _make_scoring(t_scores={"O": 50, "C": 55, "E": 35, "A": 60, "N": 45})
    mbti = _make_mbti()
    assert engine._match_condition({"lowest_domain": "E"}, scoring, mbti, "standard")
    assert not engine._match_condition({"lowest_domain": "A"}, scoring, mbti, "standard")


def test_conditional_mbti_intp(engine):
    scoring = _make_scoring()
    mbti = _make_mbti(type_code="INTP")
    assert engine._match_condition({"mbti": "INTP"}, scoring, mbti, "standard")
    assert not engine._match_condition({"mbti": "INTJ"}, scoring, mbti, "standard")


def test_conditional_mode_advanced(engine):
    scoring = _make_scoring()
    mbti = _make_mbti()
    assert engine._match_condition({"mode": "advanced"}, scoring, mbti, "advanced")
    assert not engine._match_condition({"mode": "standard"}, scoring, mbti, "advanced")


def test_conditional_mode_standard(engine):
    scoring = _make_scoring()
    mbti = _make_mbti()
    assert engine._match_condition({"mode": "standard"}, scoring, mbti, "standard")
    assert not engine._match_condition({"mode": "advanced"}, scoring, mbti, "standard")


def test_conditional_domain_threshold(engine):
    scoring = _make_scoring(t_scores={"O": 50, "C": 50, "E": 50, "A": 65, "N": 50})
    mbti = _make_mbti()
    assert engine._match_condition({"domain": "A", "ge": 60}, scoring, mbti, "standard")
    assert not engine._match_condition({"domain": "A", "ge": 70}, scoring, mbti, "standard")
    assert not engine._match_condition({"domain": "A", "le": 60}, scoring, mbti, "standard")


def test_conditional_and_or_not(engine):
    scoring = _make_scoring(t_scores={"O": 50, "C": 50, "E": 50, "A": 65, "N": 60})
    mbti = _make_mbti(type_code="INTJ", confidence=0.85)
    assert engine._match_condition({
        "and": [{"domain": "A", "ge": 60}, {"domain": "N", "ge": 55}]
    }, scoring, mbti, "standard")
    assert not engine._match_condition({
        "and": [{"domain": "A", "ge": 60}, {"domain": "O", "ge": 55}]
    }, scoring, mbti, "standard")
    assert engine._match_condition({
        "or": [{"domain": "A", "ge": 70}, {"mbti_confidence_ge": 0.8}]
    }, scoring, mbti, "standard")
    assert not engine._match_condition({
        "or": [{"domain": "A", "ge": 70}, {"domain": "O", "ge": 70}]
    }, scoring, mbti, "standard")
    assert engine._match_condition({"not": {"domain": "O", "ge": 55}}, scoring, mbti, "standard")


def test_conditional_high_neuroticism_variants(engine):
    scoring = _make_scoring(t_scores={"O": 50, "C": 50, "E": 50, "A": 50, "N": 75})
    mbti = _make_mbti(type_code="INTJ", confidence=0.5)
    assert engine._match_condition({"domain": "N", "ge": 60}, scoring, mbti, "standard")
    assert engine._match_condition({"domain": "N", "ge": 65}, scoring, mbti, "standard")


def test_conditional_no_scoring_fallback(engine):
    """Without scoring/mbti data, all eggs are available (backward compat)."""
    result = engine.trigger(lang="zh", force=True, scoring=None, mbti=None, mode="standard")
    assert result is not None
    assert isinstance(result, str)


def test_conditional_flat_true(engine):
    scoring = _make_scoring(t_scores={"O": 50, "C": 52, "E": 48, "A": 51, "N": 49})
    mbti = _make_mbti()
    assert engine._match_condition({"flat": True}, scoring, mbti, "standard")


def test_conditional_flat_edge_high(engine):
    scoring = _make_scoring(t_scores={"O": 45, "C": 55, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert engine._match_condition({"flat": True}, scoring, mbti, "standard")


def test_conditional_flat_false_on_high(engine):
    scoring = _make_scoring(t_scores={"O": 56, "C": 50, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert not engine._match_condition({"flat": True}, scoring, mbti, "standard")


def test_conditional_flat_false_on_low(engine):
    scoring = _make_scoring(t_scores={"O": 44, "C": 50, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert not engine._match_condition({"flat": True}, scoring, mbti, "standard")


def test_conditional_ge55_edge(engine):
    scoring = _make_scoring(t_scores={"O": 55, "C": 50, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert engine._match_condition({"domain": "O", "ge": 55}, scoring, mbti, "standard")


def test_conditional_ge55_below(engine):
    scoring = _make_scoring(t_scores={"O": 54, "C": 50, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert not engine._match_condition({"domain": "O", "ge": 55}, scoring, mbti, "standard")


def test_conditional_le45_edge(engine):
    scoring = _make_scoring(t_scores={"O": 45, "C": 50, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert engine._match_condition({"domain": "O", "le": 45}, scoring, mbti, "standard")


def test_conditional_le45_above(engine):
    scoring = _make_scoring(t_scores={"O": 46, "C": 50, "E": 50, "A": 50, "N": 50})
    mbti = _make_mbti()
    assert not engine._match_condition({"domain": "O", "le": 45}, scoring, mbti, "standard")


def test_conditional_coverage_all_profiles(engine):
    """Verify every user profile matches at least one egg via the full pipeline."""
    profiles = [
        # (t_scores, mode, hint)
        ({"O": 58, "C": 50, "E": 50, "A": 50, "N": 50}, "standard", "O high"),
        ({"O": 50, "C": 58, "E": 50, "A": 50, "N": 50}, "standard", "C high"),
        ({"O": 50, "C": 50, "E": 58, "A": 50, "N": 50}, "standard", "E high"),
        ({"O": 50, "C": 50, "E": 50, "A": 58, "N": 50}, "standard", "A high"),
        ({"O": 50, "C": 50, "E": 50, "A": 50, "N": 58}, "standard", "N high"),
        ({"O": 42, "C": 50, "E": 50, "A": 50, "N": 50}, "standard", "O low"),
        ({"O": 50, "C": 42, "E": 50, "A": 50, "N": 50}, "standard", "C low"),
        ({"O": 50, "C": 50, "E": 42, "A": 50, "N": 50}, "standard", "E low"),
        ({"O": 50, "C": 50, "E": 50, "A": 42, "N": 50}, "standard", "A low"),
        ({"O": 50, "C": 50, "E": 50, "A": 50, "N": 42}, "standard", "N low"),
        ({"O": 50, "C": 52, "E": 48, "A": 51, "N": 49}, "standard", "flat"),
        ({"O": 50, "C": 50, "E": 50, "A": 50, "N": 50}, "advanced", "advanced"),
        ({"O": 50, "C": 50, "E": 50, "A": 50, "N": 50}, "speed", "speed"),
    ]
    for t_scores, mode, hint in profiles:
        scoring = _make_scoring(t_scores=t_scores)
        mbti = _make_mbti()
        engine._eggs = None
        result = engine.trigger(lang="zh", force=True, scoring=scoring, mbti=mbti, mode=mode)
        assert result is not None, f"No egg matched for profile: {hint}"
