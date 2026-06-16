from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.app.db.database import get_db
from backend.app.db.repository import ReportRepository
from backend.app.schemas.models import Report

router = APIRouter(tags=["Reports & i18n"])


@router.get(
    "/report/{share_token}",
    summary="查询报告",
    description="通过 share_token 查询完整的人格测评报告，包含评分、MBTI 推断和维度解读。",
    response_model=Report,
)
def get_report(share_token: str, db: DBSession = Depends(get_db)):
    repo = ReportRepository(db)
    report = repo.get_report_by_token(share_token)
    if report is None:
        raise HTTPException(status_code=404, detail={"error": "report_not_found", "detail": "Report not found"})
    return report


@router.get(
    "/i18n/{lang}",
    summary="获取解读模板",
    description="返回指定语言的人格维度解读模板数据（JSON 格式），用于前端渲染。",
)
def get_i18n(lang: str, db: DBSession = Depends(get_db)):
    import json
    import os

    from backend.app.config import DATA_DIR

    if lang not in ("zh", "en"):
        raise HTTPException(status_code=404, detail={"error": "lang_not_found", "detail": f"Language '{lang}' not supported"})
    filepath = os.path.join(DATA_DIR, f"interpretations_{lang}.json")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail={"error": "lang_not_found", "detail": "Language file not found"})
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
