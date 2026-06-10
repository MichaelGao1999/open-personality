import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session as DBSession

from backend.app.api.questionnaire import QuestionnaireLoader
from backend.app.core.easter_egg import EasterEggEngine
from backend.app.core.mbti import MBTIInference
from backend.app.core.report_gen import ReportGenerator
from backend.app.core.scoring import ScoringEngine
from backend.app.db.database import get_db
from backend.app.db.models import Session as DBSessionModel
from backend.app.db.repository import ReportRepository
from backend.app.schemas.models import Report, SubmitRequest

router = APIRouter(prefix="/api")

questionnaire_loader = QuestionnaireLoader()
scoring_engine = ScoringEngine()
mbti_inference = MBTIInference()
report_generator = ReportGenerator()
easter_egg_engine = EasterEggEngine()


@router.get("/questionnaires/items")
def get_items(mode: str = Query("standard"), lang: str = Query("zh")):
    if mode not in ("standard", "advanced"):
        raise HTTPException(status_code=422, detail={"error": "invalid_mode", "detail": f"Mode '{mode}' not supported"})
    if lang not in ("zh", "en"):
        raise HTTPException(status_code=422, detail={"error": "invalid_lang", "detail": f"Language '{lang}' not supported"})
    try:
        items = questionnaire_loader.load_items(mode, lang)
        return {"items": [item.model_dump() for item in items]}
    except FileNotFoundError:
        raise HTTPException(status_code=422, detail={"error": "items_not_found", "detail": f"Questionnaire items not found for mode={mode} lang={lang}"})


@router.post("/questionnaires/submit")
def submit_answers(req: SubmitRequest, db: DBSession = Depends(get_db)):
    if req.mode not in ("standard", "advanced"):
        raise HTTPException(status_code=422, detail={"error": "invalid_mode", "detail": f"Mode '{req.mode}' not supported"})
    if req.lang not in ("zh", "en"):
        raise HTTPException(status_code=422, detail={"error": "invalid_lang", "detail": f"Language '{req.lang}' not supported"})

    try:
        questionnaire_loader.validate_answer_count(req.answers, req.mode)
        questionnaire_loader.validate_answer_values(req.answers)
    except ValueError as e:
        error_str = str(e)
        if "item_count_mismatch" in error_str:
            raise HTTPException(status_code=422, detail={"error": "item_count_mismatch", "detail": error_str})
        if "invalid_value" in error_str:
            raise HTTPException(status_code=422, detail={"error": "invalid_value", "detail": error_str})
        raise HTTPException(status_code=422, detail={"error": "validation_error", "detail": error_str})

    try:
        scoring_result = scoring_engine.calculate(req.answers, req.mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "scoring_failed", "detail": str(e)})

    mbti_result = mbti_inference.infer(scoring_result)
    easter_egg = easter_egg_engine.trigger(lang=req.lang)
    session_id = str(uuid.uuid4())

    report = report_generator.generate(
        scoring=scoring_result,
        mbti=mbti_result,
        easter_egg=easter_egg,
        lang=req.lang,
        session_id=session_id,
        mode=req.mode,
    )

    db_session = DBSessionModel(
        id=session_id,
        mode=req.mode,
        lang=req.lang,
        share_token=report.share_token,
        created_at=report.created_at,
    )

    repo = ReportRepository(db)
    repo.save_complete_session(db_session, req.answers, report)

    return report
