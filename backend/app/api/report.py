from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.app.db.database import get_db
from backend.app.db.repository import ReportRepository

router = APIRouter(prefix="/api")


@router.get("/report/{share_token}")
def get_report(share_token: str, db: DBSession = Depends(get_db)):
    repo = ReportRepository(db)
    report = repo.get_report_by_token(share_token)
    if report is None:
        raise HTTPException(status_code=404, detail={"error": "report_not_found", "detail": "Report not found"})
    return report


@router.get("/i18n/{lang}")
def get_i18n(lang: str, db: DBSession = Depends(get_db)):
    import json
    import os

    from backend.app.config import DATA_DIR

    if lang not in ("zh", "en"):
        raise HTTPException(status_code=404, detail={"error": "lang_not_found", "detail": f"Language '{lang}' not supported"})
    filepath = os.path.join(DATA_DIR, f"interpretations_{lang}.json")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail={"error": "lang_not_found", "detail": f"Language file not found"})
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
