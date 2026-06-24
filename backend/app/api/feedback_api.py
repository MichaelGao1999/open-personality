from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from backend.app.db.database import get_db
from backend.app.db.repository import ReportRepository
from backend.app.schemas.models import FeedbackRequest

router = APIRouter(tags=["Feedback"])


@router.post("/api/feedback")
def submit_feedback(req: FeedbackRequest, db: DBSession = Depends(get_db)):
    repo = ReportRepository(db)
    repo.save_feedback(feedback_type=req.type, content=req.content)
    return {"ok": True}
