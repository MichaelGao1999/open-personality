from pydantic import BaseModel


class AnswerItem(BaseModel):
    item_id: str
    value: int


class SubmitRequest(BaseModel):
    mode: str
    lang: str
    answers: list[AnswerItem]


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


class Report(BaseModel):
    session_id: str
    share_token: str
    mode: str
    lang: str
    scoring: ScoringResult
    mbti: MBTIResult
    interpretations: list[Interpretation]
    easter_egg: str | None
    created_at: str


class ErrorResponse(BaseModel):
    error: str
    detail: str
