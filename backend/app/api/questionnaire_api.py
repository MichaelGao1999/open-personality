from __future__ import annotations

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
from backend.app.schemas.models import QuestionnaireResponse, Report, ResumeResponse, SubmitRequest

VALID_MODES = ("standard", "advanced", "speed")
VALID_LANGS = ("zh", "en")

router = APIRouter(tags=["Questionnaires"])

questionnaire_loader = QuestionnaireLoader()
scoring_engine = ScoringEngine()
mbti_inference = MBTIInference()
report_generator = ReportGenerator()
easter_egg_engine = EasterEggEngine()


def _validate_mode_lang(mode: str, lang: str):
    if mode not in VALID_MODES:
        raise HTTPException(status_code=422, detail={"error": "invalid_mode", "detail": f"Mode '{mode}' not supported"})
    if lang not in VALID_LANGS:
        raise HTTPException(status_code=422, detail={"error": "invalid_lang", "detail": f"Language '{lang}' not supported"})


def _shuffle_round_robin(items: list) -> list:
    """将题目按 O→C→E→A→N 轮换排序，每5题覆盖全部5个维度。"""
    dim_order = ["O", "C", "E", "A", "N"]
    buckets: dict[str, list] = {d: [] for d in dim_order}
    for item in items:
        buckets[item.dimension].append(item)

    result = []
    max_len = max(len(b) for b in buckets.values())
    for i in range(max_len):
        for d in dim_order:
            if i < len(buckets[d]):
                result.append(buckets[d][i])
    return result


@router.get(
    "/questionnaires/items",
    summary="获取问卷题目",
    description="根据模式和语言返回题目列表，支持 standard（120 题）、advanced（300 题）、speed（30 题）三种模式。",
    response_model=QuestionnaireResponse,
)
def get_items(mode: str = Query("standard"), lang: str = Query("zh")):
    _validate_mode_lang(mode, lang)
    try:
        items = questionnaire_loader.load_items(mode, lang)
        items = _shuffle_round_robin(items)
        return QuestionnaireResponse(items=items)
    except FileNotFoundError:
        raise HTTPException(status_code=422, detail={"error": "items_not_found", "detail": f"Questionnaire items not found for mode={mode} lang={lang}"})


@router.post(
    "/questionnaires/submit",
    summary="提交问卷答案",
    description="提交答案并返回评分结果、MBTI 推断和人格解读。支持完整提交和部分提交（partial，用于中断恢复）。",
    response_model=Report,
)
def submit_answers(req: SubmitRequest, db: DBSession = Depends(get_db)):
    _validate_mode_lang(req.mode, req.lang)

    repo = ReportRepository(db)
    items = questionnaire_loader.load_items(req.mode, req.lang)
    total_items = len(items)

    # 如果是 partial 提交但已有 session_id，复用旧 session
    existing_session_id = req.session_id if req.status == "partial" else None
    is_partial = req.status == "partial" and len(req.answers) < total_items

    # 校验（非严格计数检查 - partial 允许不足）
    if not is_partial:
        try:
            questionnaire_loader.validate_answer_count(req.answers, req.mode)
        except ValueError as e:
            raise HTTPException(status_code=422, detail={"error": "item_count_mismatch", "detail": str(e)})

    try:
        questionnaire_loader.validate_answer_values(req.answers)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"error": "invalid_value", "detail": str(e)})

    try:
        scoring_result = scoring_engine.calculate(req.answers, req.mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "scoring_failed", "detail": str(e)})

    mbti_result = mbti_inference.infer(scoring_result)
    force_egg = req.mode == "advanced" and not is_partial
    easter_egg = easter_egg_engine.trigger(
        lang=req.lang,
        force=force_egg,
        scoring=scoring_result,
        mbti=mbti_result,
        mode=req.mode,
    )

    if existing_session_id:
        session_id = existing_session_id
        repo.save_partial_session(req.mode, req.lang, total_items,
                                                req.answers, existing_session_id)[1]
    else:
        session_id = str(uuid.uuid4())

    report = report_generator.generate(
        scoring=scoring_result,
        mbti=mbti_result,
        easter_egg=easter_egg,
        lang=req.lang,
        session_id=session_id,
        mode=req.mode,
        answered_count=len(req.answers),
        total_items=total_items,
    )

    if is_partial:
        sid, token = repo.save_partial_session(req.mode, req.lang, total_items,
                                                req.answers, existing_session_id)
        report.share_token = token
        report.session_id = sid
        # 也写入 reports 表（部分结果可查询）
        repo.save_partial_report(sid, report)
    else:
        # 完整提交
        db_session = DBSessionModel(
            id=session_id,
            mode=req.mode,
            lang=req.lang,
            status="complete",
            total_items=total_items,
            share_token=report.share_token,
            created_at=report.created_at,
        )
        repo.save_complete_session(db_session, req.answers, report)

    return report


@router.get(
    "/questionnaires/resume/{share_token}",
    summary="恢复中断的答题",
    description="通过 share_token 查询已保存的部分答题进度，返回已回答的答案列表和会话信息。",
    response_model=ResumeResponse,
)
def resume_session(share_token: str, db: DBSession = Depends(get_db)):
    repo = ReportRepository(db)
    data = repo.get_partial_session(share_token)
    if data is None:
        raise HTTPException(status_code=404, detail={"error": "session_not_found", "detail": "No partial session found for this token"})
    return ResumeResponse(
        session_id=data["session_id"],
        share_token=data["share_token"],
        mode=data["mode"],
        lang=data["lang"],
        answers=data["answers"],
        total_items=data["total_items"],
    )
