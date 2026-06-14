from __future__ import annotations

import json
import math
import os

from backend.app.config import DATA_DIR
from backend.app.schemas.models import MBTIDimension, MBTIResult, ScoringResult

class MBTIInference:
    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or DATA_DIR
        self._mapping: dict | None = None

    def _load_mapping(self) -> dict:
        if self._mapping is not None:
            return self._mapping
        filepath = os.path.join(self.data_dir, "mbti_mapping.json")
        with open(filepath, "r", encoding="utf-8") as f:
            self._mapping = json.load(f)
        return self._mapping

    def _sigmoid(self, x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    def _compute_dimension(self, scores: ScoringResult, dim_config: dict) -> tuple[float, float]:
        linear = dim_config.get("bias", 0.0)
        for domain, weight in dim_config["weights"].items():
            # 使用 t_scores（M=50, SD=10），与 McCrae & Costa 权重设计匹配
            domain_score = scores.t_scores.get(domain, 50.0)
            linear += weight * domain_score
        prob_a = self._sigmoid(linear)
        prob_b = 1.0 - prob_a
        return prob_a, prob_b

    def _compute_confidence(self, prob_a: float, prob_b: float) -> float:
        return round(abs(prob_a - prob_b), 3)

    def infer(self, big_five_scores: ScoringResult) -> MBTIResult:
        mapping = self._load_mapping()
        dimensions = []
        confidences = []
        labels = {"E_I": ("E", "I"), "S_N": ("S", "N"), "T_F": ("T", "F"), "J_P": ("J", "P")}

        for dim_key, dim_config in mapping.items():
            prob_a, prob_b = self._compute_dimension(big_five_scores, dim_config)
            label_a, label_b = labels[dim_key]
            dimensions.append(MBTIDimension(label_a=label_a, label_b=label_b, prob_a=round(prob_a, 3), prob_b=round(prob_b, 3)))
            confidences.append(self._compute_confidence(prob_a, prob_b))

        overall_confidence = round(sum(confidences) / len(confidences), 3)
        type_code = "".join(dim.label_a if dim.prob_a >= 0.5 else dim.label_b for dim in dimensions)

        return MBTIResult(dimensions=dimensions, confidence=overall_confidence, type_code=type_code)
