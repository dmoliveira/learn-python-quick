"""Optional XGBoost example with a bounded CPU budget."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.model_selection import train_test_split

from learn_python_quick.data import medical_train_test_split
from learn_python_quick.evaluation import classification_metrics
from learn_python_quick.optional import require_module


@dataclass(frozen=True, slots=True)
class BoostingRun:
    model: object
    metrics: dict[str, float]
    rounds_used: int
    train_rows: int
    validation_rows: int
    test_rows: int


def train_xgboost_classifier(
    *,
    seed: int = 42,
    max_rounds: int = 60,
) -> BoostingRun:
    """Train a small boosted-tree model with validation-based early stopping."""
    if max_rounds < 2:
        raise ValueError("max_rounds must be at least 2")
    xgboost = require_module("xgboost", extra="boost")
    classifier_type: Any = xgboost.XGBClassifier
    split = medical_train_test_split(seed=seed)
    x_train, x_validation, y_train, y_validation = train_test_split(
        split.x_train,
        split.y_train,
        test_size=0.2,
        random_state=seed,
        stratify=split.y_train,
    )
    model: Any = classifier_type(
        n_estimators=max_rounds,
        max_depth=3,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="logloss",
        early_stopping_rounds=8,
        random_state=seed,
        n_jobs=1,
        tree_method="hist",
    )
    model.fit(
        x_train,
        y_train,
        eval_set=[(x_validation, y_validation)],
        verbose=False,
    )
    predictions = np.asarray(model.predict(split.x_test))
    scores = np.asarray(model.predict_proba(split.x_test))[:, 1]
    best_iteration = getattr(model, "best_iteration", max_rounds - 1)
    return BoostingRun(
        model=model,
        metrics=classification_metrics(split.y_test, predictions, positive_scores=scores),
        rounds_used=int(best_iteration) + 1,
        train_rows=len(x_train),
        validation_rows=len(x_validation),
        test_rows=len(split.x_test),
    )
