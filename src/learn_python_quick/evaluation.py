"""Evaluation helpers for regression, classification, retrieval, and ranking."""

from __future__ import annotations

import math
from collections.abc import Sequence

from numpy.typing import ArrayLike
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)


def regression_metrics(y_true: ArrayLike, y_pred: ArrayLike) -> dict[str, float]:
    """Return complementary regression measures with stable names."""
    mse = float(mean_squared_error(y_true, y_pred))
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": math.sqrt(mse),
        "r2": float(r2_score(y_true, y_pred)),
    }


def classification_metrics(
    y_true: ArrayLike,
    y_pred: ArrayLike,
    *,
    positive_scores: ArrayLike | None = None,
) -> dict[str, float]:
    """Report balanced binary-classification basics and optional ROC-AUC."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
    }
    if positive_scores is not None:
        metrics["roc_auc"] = float(roc_auc_score(y_true, positive_scores))
    return metrics


def precision_at_k(recommended: Sequence[str], relevant: set[str], *, k: int) -> float:
    """Measure relevant items among the first ``k`` result positions."""
    _validate_k(k)
    _validate_unique_recommendations(recommended)
    top_k = recommended[:k]
    return sum(item in relevant for item in top_k) / k


def recall_at_k(recommended: Sequence[str], relevant: set[str], *, k: int) -> float:
    """Measure how many known relevant items appear in the first ``k`` positions."""
    _validate_k(k)
    _validate_unique_recommendations(recommended)
    if not relevant:
        return 0.0
    return sum(item in relevant for item in recommended[:k]) / len(relevant)


def reciprocal_rank(recommended: Sequence[str], relevant: set[str]) -> float:
    """Reward the rank of the first relevant result."""
    _validate_unique_recommendations(recommended)
    for rank, item in enumerate(recommended, start=1):
        if item in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(recommended: Sequence[str], relevant: set[str], *, k: int) -> float:
    """Compute binary normalized discounted cumulative gain."""
    _validate_k(k)
    _validate_unique_recommendations(recommended)
    dcg = sum(
        1.0 / math.log2(rank + 1)
        for rank, item in enumerate(recommended[:k], start=1)
        if item in relevant
    )
    ideal_hits = min(len(relevant), k)
    ideal_dcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / ideal_dcg if ideal_dcg else 0.0


def _validate_k(k: int) -> None:
    if k < 1:
        raise ValueError("k must be at least 1")


def _validate_unique_recommendations(recommended: Sequence[str]) -> None:
    if len(set(recommended)) != len(recommended):
        raise ValueError("recommended item IDs must be unique")
