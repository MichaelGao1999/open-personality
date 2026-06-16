from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone

from backend.app.config import DATA_DIR
from backend.app.schemas.models import (
    Interpretation,
    MBTIResult,
    Report,
    ScoringResult,
)

class ReportGenerator:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or DATA_DIR
        self._interpretations: dict | None = None

    def _load_interpretations(self, lang: str) -> dict:
        filepath = os.path.join(self.data_dir, f"interpretations_{lang}.json")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _interpret_domain(self, score: float, high_text: dict, low_text: dict) -> tuple[str, str]:
        if score >= 55:
            return high_text.get("title", "较高"), high_text.get("body", "你的得分较高。")
        elif score <= 45:
            return low_text.get("title", "较低"), low_text.get("body", "你的得分较低。")
        return "中等", "你的得分处于中间范围。"

    def generate(
        self,
        scoring: ScoringResult,
        mbti: MBTIResult,
        easter_egg: str | None,
        lang: str,
        session_id: str,
        mode: str,
        answered_count: int = 0,
        total_items: int = 0,
    ) -> Report:
        interpretations_data = self._load_interpretations(lang)
        interpretations_en = self._load_interpretations("en")

        interpretations = []
        for dim in ["O", "C", "E", "A", "N"]:
            dim_data = interpretations_data.get(dim, {})
            t_score = scoring.t_scores.get(dim, 50.0)
            title_zh, body_zh = self._interpret_domain(t_score, dim_data.get("high", {}), dim_data.get("low", {}))
            en_data = interpretations_en.get(dim, {})
            title_en, body_en = self._interpret_domain(t_score, en_data.get("high", {}), en_data.get("low", {}))
            interpretations.append(Interpretation(
                dimension=dim, title_zh=title_zh, title_en=title_en,
                body_zh=body_zh, body_en=body_en,
            ))

        for facet_key in sorted(scoring.facet_scores.keys()):
            dim_data = interpretations_data.get(facet_key, {})
            f_score = scoring.facet_scores.get(facet_key, 50.0)
            title_zh, body_zh = self._interpret_domain(f_score, dim_data.get("high", {}), dim_data.get("low", {}))
            en_data = interpretations_en.get(facet_key, {})
            title_en, body_en = self._interpret_domain(f_score, en_data.get("high", {}), en_data.get("low", {}))
            interpretations.append(Interpretation(
                dimension=facet_key, title_zh=title_zh, title_en=title_en,
                body_zh=body_zh, body_en=body_en,
            ))

        now = datetime.now(timezone.utc).isoformat()
        share_token = self._generate_share_token()

        return Report(
            session_id=session_id,
            share_token=share_token,
            mode=mode,
            lang=lang,
            scoring=scoring,
            mbti=mbti,
            interpretations=interpretations,
            easter_egg=easter_egg,
            created_at=now,
            answered_count=answered_count,
            total_items=total_items,
        )

    def _generate_share_token(self) -> str:
        import base64
        import hashlib
        raw = hashlib.sha256(str(uuid.uuid4()).encode()).digest()
        token = base64.b64encode(raw, altchars=b"AB").decode()[:8]
        return token
