"""Solution: select a deterministic threshold under a recall constraint."""

from __future__ import annotations

import math
from collections.abc import Sequence
from numbers import Integral, Real


def _validated_probability(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must contain finite real numbers")
    normalized = float(value)
    if not math.isfinite(normalized) or not 0.0 <= normalized <= 1.0:
        raise ValueError(f"{name} must contain values from 0.0 through 1.0")
    return normalized


def select_decision_threshold(
    y_true: Sequence[int],
    probabilities: Sequence[float],
    minimum_recall: float,
) -> dict[str, float | int]:
    if not y_true or not probabilities:
        raise ValueError("labels and probabilities must not be empty")
    if len(y_true) != len(probabilities):
        raise ValueError("labels and probabilities must have equal length")

    labels: list[int] = []
    for label in y_true:
        if isinstance(label, bool) or not isinstance(label, Integral) or label not in (0, 1):
            raise ValueError("labels must be integer 0 or 1")
        labels.append(int(label))

    scores = [_validated_probability(value, name="probabilities") for value in probabilities]
    recall_floor = _validated_probability(minimum_recall, name="minimum_recall")
    if recall_floor == 0.0:
        raise ValueError("minimum_recall must be greater than 0.0")

    positive_count = sum(labels)
    if positive_count == 0:
        raise ValueError("labels must contain at least one positive")

    best_key: tuple[float, float] | None = None
    best_result: dict[str, float | int] | None = None
    for threshold in sorted(set(scores), reverse=True):
        predictions = [score >= threshold for score in scores]
        predicted_positive = sum(predictions)
        true_positive = sum(
            label == 1 and prediction for label, prediction in zip(labels, predictions, strict=True)
        )
        recall = true_positive / positive_count
        if recall < recall_floor:
            continue
        precision = true_positive / predicted_positive
        candidate_key = (precision, threshold)
        if best_key is None or candidate_key > best_key:
            best_key = candidate_key
            best_result = {
                "threshold": float(threshold),
                "precision": float(precision),
                "recall": float(recall),
                "predicted_positive": int(predicted_positive),
            }

    if best_result is None:  # The lowest observed score always reaches recall 1.0.
        raise RuntimeError("no threshold met a valid recall floor")
    return best_result
