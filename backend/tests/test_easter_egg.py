from pathlib import Path

import pytest

from backend.app.core.easter_egg import EasterEggEngine


@pytest.fixture
def engine():
    data_dir = str(Path(__file__).resolve().parent.parent / "data")
    return EasterEggEngine(data_dir=data_dir)


def test_trigger_rate_approximate(engine):
    results = []
    engine._eggs = None
    for _ in range(1000):
        engine._eggs = None
        results.append(engine.trigger(lang="en", seed=str(_)))
    triggered = [r for r in results if r is not None]
    rate = len(triggered) / 1000
    assert 0.07 <= rate <= 0.13, f"Trigger rate {rate} outside expected 7-13%"


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
    for egg in eggs_data.get("medium", []):
        assert egg.get("zh") and len(egg["zh"]) > 0
        assert egg.get("en") and len(egg["en"]) > 0


def test_trigger_rate_config(engine):
    eggs_data = engine._load_eggs()
    assert eggs_data["trigger_rate"] == 0.1
