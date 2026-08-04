"""Evaluation helpers for regression, classification, retrieval, and ranking."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray
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
    true_values, predicted_values = _validated_regression_pair(y_true, y_pred)
    mse = float(mean_squared_error(true_values, predicted_values))
    return {
        "mae": float(mean_absolute_error(true_values, predicted_values)),
        "rmse": math.sqrt(mse),
        "r2": float(r2_score(true_values, predicted_values)),
    }


def classification_metrics(
    y_true: ArrayLike,
    y_pred: ArrayLike,
    *,
    positive_scores: ArrayLike | None = None,
) -> dict[str, float]:
    """Report balanced binary-classification basics and optional ROC-AUC."""
    true_values, predicted_values = _validated_classification_pair(y_true, y_pred)
    labels = [*true_values.tolist(), *predicted_values.tolist()]
    if any(label not in (0, 1) for label in labels):
        raise ValueError("classification labels must be 0 or 1")

    metrics = {
        "accuracy": float(accuracy_score(true_values, predicted_values)),
        "precision": float(precision_score(true_values, predicted_values, zero_division=0)),
        "recall": float(recall_score(true_values, predicted_values, zero_division=0)),
        "f1": float(f1_score(true_values, predicted_values, zero_division=0)),
    }
    if positive_scores is not None:
        scores = np.asarray(positive_scores)
        if scores.ndim != 1:
            raise ValueError("positive_scores must be one-dimensional")
        if len(scores) != len(true_values):
            raise ValueError("positive_scores must match y_true length")
        if not np.issubdtype(scores.dtype, np.number) or not np.isfinite(scores).all():
            raise ValueError("positive_scores must contain finite numbers")
        if len(set(true_values.tolist())) != 2:
            raise ValueError("ROC-AUC requires both classes in y_true")
        metrics["roc_auc"] = float(roc_auc_score(true_values, scores))
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


def _validated_classification_pair(
    y_true: ArrayLike,
    y_pred: ArrayLike,
) -> tuple[NDArray[Any], NDArray[Any]]:
    true_values = np.asarray(y_true)
    predicted_values = np.asarray(y_pred)
    if true_values.ndim != 1 or predicted_values.ndim != 1:
        raise ValueError("y_true and y_pred must be one-dimensional")
    if true_values.size == 0:
        raise ValueError("y_true and y_pred must not be empty")
    if len(true_values) != len(predicted_values):
        raise ValueError("y_true and y_pred must have equal length")
    return true_values, predicted_values


def _validated_regression_pair(
    y_true: ArrayLike,
    y_pred: ArrayLike,
) -> tuple[NDArray[Any], NDArray[Any]]:
    true_values = np.asarray(y_true)
    predicted_values = np.asarray(y_pred)
    if true_values.ndim not in {1, 2} or predicted_values.ndim not in {1, 2}:
        raise ValueError("regression targets must be one- or two-dimensional")
    if true_values.size == 0 or predicted_values.size == 0:
        raise ValueError("y_true and y_pred must not be empty")
    if true_values.shape != predicted_values.shape:
        raise ValueError("y_true and y_pred must have equal shape")
    return true_values, predicted_values
