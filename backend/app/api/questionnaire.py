from __future__ import annotations

import json
import os

from backend.app.config import DATA_DIR

from backend.app.schemas.models import AnswerItem, QuestionnaireItem


class QuestionnaireLoader:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or DATA_DIR
        self._cache: dict[str, list[dict]] = {}

    def load_items(self, mode: str, lang: str) -> list[QuestionnaireItem]:
        cache_key = f"{mode}_{lang}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        mode_key = {"standard": "120", "advanced": "300", "speed": "_speed"}.get(mode, "120")
        filepath = os.path.join(self.data_dir, "items", f"ipip{mode_key}_{lang}.json")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = [QuestionnaireItem(**item) for item in data["items"]]
        self._cache[cache_key] = items
        return items

    def validate_answer_count(self, answers: list[AnswerItem], mode: str) -> None:
        expected = {"standard": 120, "advanced": 300, "speed": 30}.get(mode, 120)
        if len(answers) != expected:
            raise ValueError(f"item_count_mismatch: expected {expected} answers, got {len(answers)}")

    def validate_answer_values(self, answers: list[AnswerItem]) -> None:
        for ans in answers:
            if ans.value < 1 or ans.value > 5:
                raise ValueError(f"invalid_value: item {ans.item_id} has value {ans.value}, expected 1-5")
