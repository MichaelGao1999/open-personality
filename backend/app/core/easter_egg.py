from __future__ import annotations

import json
import os
import random

from backend.app.config import DATA_DIR


class EasterEggEngine:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or DATA_DIR
        self._eggs: dict | None = None

    def _load_eggs(self) -> dict:
        if self._eggs is not None:
            return self._eggs
        filepath = os.path.join(self.data_dir, "easter_eggs.json")
        with open(filepath, "r", encoding="utf-8") as f:
            self._eggs = json.load(f)
        return self._eggs

    _TRIGGER_RATES = {"standard": 0.5, "speed": 0.1}

    def _roll(self, mode: str = "standard") -> bool:
        rate = self._TRIGGER_RATES.get(mode, 0.1)
        return random.random() < rate

    def _match_condition(self, condition: dict, scoring, mbti, mode: str) -> bool:
        if not condition:
            return True

        if "and" in condition:
            return all(self._match_condition(c, scoring, mbti, mode) for c in condition["and"])

        if "or" in condition:
            return any(self._match_condition(c, scoring, mbti, mode) for c in condition["or"])

        if "not" in condition:
            return not self._match_condition(condition["not"], scoring, mbti, mode)

        if "highest_domain" in condition:
            target = condition["highest_domain"]
            if not scoring or not scoring.t_scores:
                return False
            max_domain = max(scoring.t_scores, key=scoring.t_scores.get)
            return max_domain == target  # type: ignore[no-any-return]

        if "lowest_domain" in condition:
            target = condition["lowest_domain"]
            if not scoring or not scoring.t_scores:
                return False
            min_domain = min(scoring.t_scores, key=scoring.t_scores.get)
            return min_domain == target  # type: ignore[no-any-return]

        if "highest_facet" in condition:
            target = condition["highest_facet"]
            if not scoring or not scoring.facet_scores:
                return False
            max_facet = max(scoring.facet_scores, key=scoring.facet_scores.get)
            return max_facet == target  # type: ignore[no-any-return]

        if "lowest_facet" in condition:
            target = condition["lowest_facet"]
            if not scoring or not scoring.facet_scores:
                return False
            min_facet = min(scoring.facet_scores, key=scoring.facet_scores.get)
            return min_facet == target  # type: ignore[no-any-return]

        if "domain" in condition:
            score = scoring.t_scores.get(condition["domain"], 50) if scoring else 50
            if "ge" in condition and score < condition["ge"]:
                return False
            if "le" in condition and score > condition["le"]:
                return False
            return True

        if "facet" in condition:
            score = scoring.facet_scores.get(condition["facet"], 50) if scoring else 50
            if "ge" in condition and score < condition["ge"]:
                return False
            if "le" in condition and score > condition["le"]:
                return False
            return True

        if "mbti" in condition:
            return mbti is not None and mbti.type_code == condition["mbti"]

        if "mbti_in" in condition:
            return mbti is not None and mbti.type_code in condition["mbti_in"]

        if "mbti_dim" in condition:
            if mbti is None:
                return False
            dim = condition["mbti_dim"]
            axis = dim["axis"]
            prefer = dim["prefer"]
            min_prob = dim.get("min_prob", 0.0)
            for d in mbti.dimensions:
                if all(x in [d.label_a, d.label_b] for x in [axis[:1], axis[-1:]]):
                    if d.label_a == prefer:
                        return d.prob_a >= min_prob  # type: ignore[no-any-return]
                    elif d.label_b == prefer:
                        return d.prob_b >= min_prob  # type: ignore[no-any-return]
            return False

        if "mbti_confidence_ge" in condition:
            return mbti is not None and mbti.confidence >= condition["mbti_confidence_ge"]

        if "mbti_confidence_le" in condition:
            return mbti is not None and mbti.confidence <= condition["mbti_confidence_le"]

        if "mode" in condition:
            return mode == condition["mode"]  # type: ignore[no-any-return]

        if "mode_in" in condition:
            return mode in condition["mode_in"]

        if "flat" in condition and condition["flat"]:
            if not scoring or not scoring.t_scores:
                return False
            return all(45 <= v <= 55 for v in scoring.t_scores.values())

        return True

    def _pick_conditional(self, lang: str, scoring, mbti, mode: str) -> str:
        eggs_data = self._load_eggs()
        pool = []
        has_data = scoring is not None and mbti is not None
        for egg in eggs_data.get("eggs", []):
            if not has_data:
                pool.append(egg.get(lang, egg.get("en", "")))
            else:
                condition = egg.get("condition", {})
                if self._match_condition(condition, scoring, mbti, mode):
                    pool.append(egg.get(lang, egg.get("en", "")))
        for egg in eggs_data.get("medium", []):
            if not has_data:
                pool.append(egg.get(lang, egg.get("en", "")))
            else:
                condition = egg.get("condition", {})
                if self._match_condition(condition, scoring, mbti, mode):
                    pool.append(egg.get(lang, egg.get("en", "")))
        if not pool:
            return ""
        return random.choice(pool)  # type: ignore[no-any-return]

    def trigger(
        self,
        lang: str = "zh",
        seed: str | None = None,
        force: bool = False,
        scoring=None,
        mbti=None,
        mode: str = "standard",
    ) -> str | None:
        if seed is not None:
            random.seed(seed)
        if not force and not self._roll(mode):
            return None
        result = self._pick_conditional(lang, scoring, mbti, mode)
        return result if result else None
