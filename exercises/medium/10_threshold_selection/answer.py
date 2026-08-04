"""Learner answer for the decision-threshold exercise."""

from __future__ import annotations

from collections.abc import Sequence


def select_decision_threshold(
    y_true: Sequence[int],
    probabilities: Sequence[float],
    minimum_recall: float,
) -> dict[str, float | int]:
    """Select a threshold using the exercise's validation-data rule."""
    raise NotImplementedError("Implement select_decision_threshold using the exercise contract")
