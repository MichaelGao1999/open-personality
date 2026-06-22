# mypy: ignore-errors
from __future__ import annotations

import json
import random
import string
import uuid
from datetime import datetime, timezone

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

    def save_partial_session(self, mode: str, lang: str, total_items: int, answers: list[AnswerItem],
                             existing_session_id: str | None = None) -> tuple[str, str]:
        """保存部分答题进度。返回 (session_id, share_token)"""
        try:
            if existing_session_id:
                session = self.db.query(DBSessionModel).filter(
                    DBSessionModel.id == existing_session_id
                ).first()
                if session:
                    session_id = existing_session_id
                    share_token = session.share_token
                    # 覆盖旧的 answers
                    self.db.query(Answer).filter(Answer.session_id == session_id).delete()
                else:
                    return self._create_new_partial(mode, lang, total_items, answers)
            else:
                return self._create_new_partial(mode, lang, total_items, answers)

            db_answers = [
                Answer(session_id=session_id, item_id=a.item_id, value=a.value) for a in answers
            ]
            self.db.add_all(db_answers)
            self.db.commit()
            return session_id, share_token
        except Exception:
            self.db.rollback()
            raise

    def _create_new_partial(self, mode: str, lang: str, total_items: int, answers: list[AnswerItem]) -> tuple[str, str]:
        session_id = str(uuid.uuid4())
        chars = string.ascii_letters + string.digits
        share_token = "".join(random.choices(chars, k=8))
        session = DBSessionModel(
            id=session_id,
            mode=mode,
            lang=lang,
            status="partial",
            total_items=total_items,
            share_token=share_token,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.db.add(session)
        self.db.flush()
        db_answers = [
            Answer(session_id=session_id, item_id=a.item_id, value=a.value) for a in answers
        ]
        self.db.add_all(db_answers)
        self.db.commit()
        return session_id, share_token

    def save_partial_report(self, session_id: str, report: Report) -> None:
        """保存或更新报告到 reports 表（用于部分结果查询）"""
        try:
            existing = self.db.query(DBReport).filter(
                DBReport.session_id == session_id
            ).first()
            if existing:
                existing.big_five_scores = report.scoring.model_dump_json()
                existing.mbti_result = report.mbti.model_dump_json()
                existing.interpretations = json.dumps([i.model_dump() for i in report.interpretations])
                existing.easter_egg = report.easter_egg
                existing.created_at = report.created_at
            else:
                db_report = DBReport(
                    session_id=session_id,
                    big_five_scores=report.scoring.model_dump_json(),
                    mbti_result=report.mbti.model_dump_json(),
                    interpretations=json.dumps([i.model_dump() for i in report.interpretations]),
                    easter_egg=report.easter_egg,
                    created_at=report.created_at,
                )
                self.db.add(db_report)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def get_partial_session(self, share_token: str) -> dict | None:
        session = self.db.query(DBSessionModel).filter(
            DBSessionModel.share_token == share_token,
            DBSessionModel.status.in_(["partial", "active"]),
        ).first()
        if session is None:
            return None
        db_answers = self.db.query(Answer).filter(Answer.session_id == session.id).all()
        return {
            "session_id": session.id,
            "share_token": session.share_token,
            "mode": session.mode,
            "lang": session.lang,
            "answers": [AnswerItem(item_id=a.item_id, value=a.value) for a in db_answers],
            "total_items": session.total_items or 0,
        }

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
        answered = self.db.query(Answer).filter(Answer.session_id == session.id).count()
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
            answered_count=answered,
            total_items=session.total_items or 0,
        )
