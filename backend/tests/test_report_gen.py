from pathlib import Path

import pytest

from backend.app.core.mbti import MBTIInference
from backend.app.core.report_gen import ReportGenerator
from backend.app.core.scoring import ScoringEngine
from backend.app.schemas.models import AnswerItem


@pytest.fixture
def data_dir():
    return str(Path(__file__).resolve().parent.parent / "data")


@pytest.fixture
def generator(data_dir):
    return ReportGenerator(data_dir=data_dir)


@pytest.fixture
def engine(data_dir):
    return ScoringEngine(data_dir=data_dir)


@pytest.fixture
def inference(data_dir):
    return MBTIInference(data_dir=data_dir)


def test_generate_full_report(generator, engine, inference):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]
    scoring = engine.calculate(answers, "standard")
    mbti = inference.infer(scoring)
    report = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg="Test egg",
        lang="zh", session_id="test-session-1", mode="standard",
    )
    assert report.session_id == "test-session-1"
    assert report.share_token is not None
    assert len(report.share_token) == 8
    assert report.mode == "standard"
    assert report.lang == "zh"
    assert report.easter_egg == "Test egg"
    assert len(report.interpretations) == 35


def test_report_fields_non_empty(generator, engine, inference):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=4) for i in range(1, 121)]
    scoring = engine.calculate(answers, "standard")
    mbti = inference.infer(scoring)
    report = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg=None,
        lang="en", session_id="test-session-2", mode="standard",
    )
    assert report.session_id is not None
    assert report.share_token is not None
    assert report.scoring is not None
    assert report.mbti is not None
    assert report.interpretations is not None


def test_language_switch(generator, engine, inference):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]
    scoring = engine.calculate(answers, "standard")
    mbti = inference.infer(scoring)
    report_zh = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg=None,
        lang="zh", session_id="test-zh", mode="standard",
    )
    report_en = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg=None,
        lang="en", session_id="test-en", mode="standard",
    )
    for iz, ie in zip(report_zh.interpretations, report_en.interpretations):
        assert iz.dimension == ie.dimension
        assert iz.title_zh != ""
        assert iz.title_en != ""
        assert iz.body_zh != ""
        assert iz.body_en != ""


def test_easter_egg_optional(generator, engine, inference):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]
    scoring = engine.calculate(answers, "standard")
    mbti = inference.infer(scoring)
    report_with = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg="Surprise!",
        lang="zh", session_id="test-egg-1", mode="standard",
    )
    report_without = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg=None,
        lang="zh", session_id="test-egg-2", mode="standard",
    )
    assert report_with.easter_egg == "Surprise!"
    assert report_without.easter_egg is None


def test_share_token_format(generator, engine, inference):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]
    scoring = engine.calculate(answers, "standard")
    mbti = inference.infer(scoring)
    report = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg=None,
        lang="zh", session_id="test-token", mode="standard",
    )
    assert len(report.share_token) == 8
    assert all(c.isalnum() for c in report.share_token)


def test_all_interpretations_have_keys(generator, engine, inference):
    answers = [AnswerItem(item_id=f"ipip_{i:03d}", value=3) for i in range(1, 121)]
    scoring = engine.calculate(answers, "standard")
    mbti = inference.infer(scoring)
    report = generator.generate(
        scoring=scoring, mbti=mbti, easter_egg=None,
        lang="zh", session_id="test-keys", mode="standard",
    )
    for interp in report.interpretations:
        assert interp.dimension in ["O", "C", "E", "A", "N"] or interp.dimension.startswith(
            ("O_", "C_", "E_", "A_", "N_")
        )
