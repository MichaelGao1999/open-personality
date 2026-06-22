from __future__ import annotations

import json
import os

from backend.app.config import DATA_DIR
from backend.app.schemas.models import AnswerItem, ScoringResult

class ScoringEngine:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or DATA_DIR
        self._items_cache: dict[str, dict] = {}

    def _load_items(self, mode: str, lang: str) -> list[dict]:
        cache_key = f"{mode}_{lang}"
        if cache_key in self._items_cache:
            return self._items_cache[cache_key]  # type: ignore[return-value]
        mode_map = {"standard": "120", "advanced": "300", "speed": "_speed"}
        mode_key = mode_map.get(mode, "120")
        filename = f"ipip{mode_key}_{lang}.json"
        filepath = os.path.join(self.data_dir, "items", filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._items_cache[cache_key] = data["items"]
        return data["items"]  # type: ignore[no-any-return]  # type: ignore[no-any-return]

    def _load_norms(self) -> dict:
        filepath = os.path.join(self.data_dir, "norms.json")
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)  # type: ignore[no-any-return]  # type: ignore[no-any-return]

    def _compute_domain_raw(self, answers: list[AnswerItem], items: list[dict]) -> dict[str, float]:
        item_map = {item["item_id"]: item for item in items}
        dim_items: dict[str, list[int]] = {}
        for ans in answers:
            item = item_map.get(ans.item_id)
            if item is None:
                continue
            dim = item["dimension"]
            if dim not in dim_items:
                dim_items[dim] = []
            score = ans.value
            if item["reversed"]:
                score = 6 - score
            dim_items[dim].append(score)
        return {dim: sum(scores) / len(scores) * 24 if scores else 0.0 for dim, scores in dim_items.items()}

    def _compute_facet_raw(self, answers: list[AnswerItem], items: list[dict]) -> dict[str, float]:
        item_map = {item["item_id"]: item for item in items}
        facet_items: dict[str, list[int]] = {}
        for ans in answers:
            item = item_map.get(ans.item_id)
            if item is None:
                continue
            facet = item["facet"]
            if facet not in facet_items:
                facet_items[facet] = []
            score = ans.value
            if item["reversed"]:
                score = 6 - score
            facet_items[facet].append(score)
        result: dict[str, float] = {}
        for facet, scores in facet_items.items():
            if len(scores) == 4:
                result[facet] = sum(scores) * 6
            else:
                raw_sum = sum(scores)
                result[facet] = raw_sum / len(scores) * 24 if scores else 0.0  # type: ignore[assignment]
        return result  # type: ignore[return-value]

    def _normalize(self, raw_scores: dict[str, float], norms: dict) -> dict[str, float]:
        t_scores = {}
        for key, raw in raw_scores.items():
            norm = norms.get(key, {"mean": 50.0, "sd": 10.0})
            t = 50 + 10 * ((raw - norm["mean"]) / norm["sd"]) if norm["sd"] else 50.0
            t_scores[key] = round(t, 1)
        return t_scores

    def calculate(self, answers: list[AnswerItem], mode: str) -> ScoringResult:
        mode_key = "120" if mode == "standard" else "300"
        items = self._load_items(mode_key, "zh")
        norms = self._load_norms()
        raw_domains = self._compute_domain_raw(answers, items)
        raw_facets = self._compute_facet_raw(answers, items)
        raw_all = {**raw_domains, **raw_facets}
        t_all = self._normalize(raw_all, norms)
        raw_scores = {k: round(v, 1) for k, v in raw_domains.items()}
        t_scores = {k: t_all[k] for k in raw_domains}
        facet_scores = {k: t_all[k] for k in raw_facets}
        return ScoringResult(raw_scores=raw_scores, t_scores=t_scores, facet_scores=facet_scores)
