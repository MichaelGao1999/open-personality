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

    def _roll(self) -> bool:
        return random.random() < 0.1

    def _pick(self, lang: str) -> str:
        eggs_data = self._load_eggs()
        pool = []
        for egg in eggs_data.get("eggs", []):
            pool.append((egg["id"], egg.get(lang, egg.get("en", ""))))
        for egg in eggs_data.get("medium", []):
            pool.append((egg["id"], egg.get(lang, egg.get("en", ""))))
        if not pool:
            return ""
        return random.choice(pool)[1]  # type: ignore[no-any-return]

    def trigger(self, lang: str = "zh", seed: str | None = None, force: bool = False) -> str | None:
        if seed is not None:
            random.seed(seed)
        if not force and not self._roll():
            return None
        return self._pick(lang)
