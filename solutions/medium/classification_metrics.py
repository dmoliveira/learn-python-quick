"""Solution: validate binary labels, then calculate complementary metrics."""

from __future__ import annotations

from collections.abc import Sequence

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def evaluate_binary_classifier(
    y_true: Sequence[int],
    y_pred: Sequence[int],
) -> dict[str, object]:
    if not y_true or not y_pred:
        raise ValueError("label sequences must not be empty")
    if len(y_true) != len(y_pred):
        raise ValueError("label sequences must have equal length")
    if not set(y_true).issubset({0, 1}) or not set(y_pred).issubset({0, 1}):
        raise ValueError("labels must be 0 or 1")

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
    }
