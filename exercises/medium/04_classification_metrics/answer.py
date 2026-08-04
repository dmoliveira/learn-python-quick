"""Learner answer for the binary classification metrics exercise."""

from __future__ import annotations

from collections.abc import Sequence


def evaluate_binary_classifier(
    y_true: Sequence[int],
    y_pred: Sequence[int],
) -> dict[str, object]:
    """Calculate binary metrics and a stable 2-by-2 confusion matrix."""
    raise NotImplementedError("Implement evaluate_binary_classifier using the exercise contract")
