"""Leakage-safe, deterministic scikit-learn training examples."""

from __future__ import annotations

from dataclasses import dataclass

from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from learn_python_quick.data import load_regression_data, medical_train_test_split
from learn_python_quick.evaluation import classification_metrics, regression_metrics


@dataclass(frozen=True, slots=True)
class TrainingRun:
    """Keep the fitted model next to the evidence used to compare it."""

    model: ClassifierMixin | RegressorMixin
    metrics: dict[str, float]
    train_rows: int
    test_rows: int


def build_logistic_pipeline(*, seed: int = 42) -> Pipeline:
    """Fit scaling inside each training split, preventing preprocessing leakage."""
    return Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "model",
                LogisticRegression(max_iter=1_000, random_state=seed),
            ),
        ]
    )


def train_medical_classifier(*, seed: int = 42) -> TrainingRun:
    """Train and evaluate a small binary classifier on packaged data."""
    split = medical_train_test_split(seed=seed)
    model = build_logistic_pipeline(seed=seed)
    model.fit(split.x_train, split.y_train)
    predictions = model.predict(split.x_test)
    scores = model.predict_proba(split.x_test)[:, 1]
    return TrainingRun(
        model=model,
        metrics=classification_metrics(split.y_test, predictions, positive_scores=scores),
        train_rows=len(split.x_train),
        test_rows=len(split.x_test),
    )


def compare_tree_models(*, seed: int = 42) -> dict[str, float]:
    """Compare interpretable and ensemble tree baselines on one fixed split."""
    split = medical_train_test_split(seed=seed)
    models: dict[str, ClassifierMixin] = {
        "decision_tree": DecisionTreeClassifier(max_depth=4, random_state=seed),
        "random_forest": RandomForestClassifier(
            n_estimators=80,
            max_depth=6,
            random_state=seed,
            n_jobs=1,
        ),
    }
    scores: dict[str, float] = {}
    for name, model in models.items():
        model.fit(split.x_train, split.y_train)
        scores[name] = float(model.score(split.x_test, split.y_test))
    return scores


def train_diabetes_regression(*, alpha: float = 1.0) -> TrainingRun:
    """Train a regularized linear baseline and report error in target units."""
    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    features, target = load_regression_data()
    split_at = int(len(features) * 0.8)
    x_train, x_test = features.iloc[:split_at], features.iloc[split_at:]
    y_train, y_test = target.iloc[:split_at], target.iloc[split_at:]
    model = Pipeline([("scale", StandardScaler()), ("model", Ridge(alpha=alpha))])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return TrainingRun(
        model=model,
        metrics=regression_metrics(y_test, predictions),
        train_rows=len(x_train),
        test_rows=len(x_test),
    )
