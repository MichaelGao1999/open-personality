from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class AnswerItem(BaseModel):
    item_id: str
    value: int


class SubmitRequest(BaseModel):
    mode: str
    lang: str
    answers: list[AnswerItem]
    status: str = "complete"  # "partial" | "complete"
    session_id: Optional[str] = None  # resume 时传递已有 session_id


class QuestionnaireItem(BaseModel):
    item_id: str
    dimension: str
    facet: str
    text: str
    reversed: bool


class QuestionnaireResponse(BaseModel):
    items: list[QuestionnaireItem]


class ScoringResult(BaseModel):
    raw_scores: dict[str, float]
    t_scores: dict[str, float]
    facet_scores: dict[str, float]


class MBTIDimension(BaseModel):
    label_a: str
    label_b: str
    prob_a: float
    prob_b: float


class MBTIResult(BaseModel):
    dimensions: list[MBTIDimension]
    confidence: float
    type_code: str


class Interpretation(BaseModel):
    dimension: str
    title_zh: str
    title_en: str
    body_zh: str
    body_en: str
    body_high_zh: str = ""
    body_low_zh: str = ""
    body_high_en: str = ""
    body_low_en: str = ""
    definition_zh: str = ""
    definition_en: str = ""


class Report(BaseModel):
    session_id: str
    share_token: str
    mode: str
    lang: str
    scoring: ScoringResult
    mbti: MBTIResult
    interpretations: list[Interpretation]
    easter_egg: Optional[str]
    created_at: str
    answered_count: int = 0
    total_items: int = 0


class ResumeResponse(BaseModel):
    session_id: str
    share_token: str
    mode: str
    lang: str
    answers: list[AnswerItem]
    total_items: int


class ErrorResponse(BaseModel):
    error: str
    detail: str
