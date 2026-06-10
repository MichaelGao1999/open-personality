import json
import uuid

from sqlalchemy.orm import Session as DBSession

from backend.app.db.models import Answer, Report as DBReport, Session as DBSessionModel
from backend.app.schemas.models import AnswerItem, Report


class ReportRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def save_complete_session(self, session_model: DBSessionModel, answers: list[AnswerItem], report: Report) -> str:
        try:
            self.db.add(session_model)
            self.db.flush()
            db_answers = [
                Answer(session_id=session_model.id, item_id=a.item_id, value=a.value)
                for a in answers
            ]
            self.db.add_all(db_answers)
            db_report = DBReport(
                session_id=session_model.id,
                big_five_scores=report.scoring.model_dump_json(),
                mbti_result=report.mbti.model_dump_json(),
                interpretations=json.dumps([i.model_dump() for i in report.interpretations]),
                easter_egg=report.easter_egg,
                created_at=report.created_at,
            )
            self.db.add(db_report)
            self.db.commit()
            return session_model.id
        except Exception:
            self.db.rollback()
            raise

    def get_report_by_token(self, share_token: str) -> Report | None:
        session = self.db.query(DBSessionModel).filter(
            DBSessionModel.share_token == share_token
        ).first()
        if session is None:
            return None
        db_report = self.db.query(DBReport).filter(
            DBReport.session_id == session.id
        ).first()
        if db_report is None:
            return None
        return Report(
            session_id=session.id,
            share_token=session.share_token,
            mode=session.mode,
            lang=session.lang,
            scoring=json.loads(db_report.big_five_scores),
            mbti=json.loads(db_report.mbti_result),
            interpretations=json.loads(db_report.interpretations),
            easter_egg=db_report.easter_egg,
            created_at=db_report.created_at,
        )
