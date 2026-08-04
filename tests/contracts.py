"""Public behavior contracts shared by learners and official solutions."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from typing import Any

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from pydantic import ValidationError
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

SalesFunction = Callable[[list[dict[str, object]]], dict[str, object]]
LogFunction = Callable[[list[str]], dict[str, object]]
FeatureFunction = Callable[[pd.DataFrame], pd.DataFrame]
MetricFunction = Callable[[Sequence[int], Sequence[int]], dict[str, object]]
PipelineFunction = Callable[..., Pipeline]
RecommendFunction = Callable[..., list[str]]
JobBatchFunction = Callable[..., dict[str, object]]
TrainingConfigFunction = Callable[[Mapping[str, object]], dict[str, object]]
MissingValueFunction = Callable[[pd.DataFrame], pd.DataFrame]
ThresholdFunction = Callable[[Sequence[int], Sequence[float], float], dict[str, object]]
TensorBatchFunction = Callable[..., list[tuple[Any, Any]]]
PredictionEnvelopeFunction = Callable[..., dict[str, object]]


def check_sales_summary(function: SalesFunction) -> None:
    rows: list[dict[str, object]] = [
        {"product": "coffee", "units": 2, "unit_price": 4.5},
        {"product": "tea", "units": 3, "unit_price": 3.25},
        {"product": "coffee", "units": 1, "unit_price": 4.5},
    ]
    assert function(rows) == {
        "revenue": 23.25,
        "units_by_product": {"coffee": 3, "tea": 3},
        "best_seller": "coffee",
    }
    assert function([]) == {"revenue": 0.0, "units_by_product": {}, "best_seller": None}
    with pytest.raises(ValueError, match=r".+"):
        function([{"product": "tea", "units": -1, "unit_price": 3.0}])
    with pytest.raises(ValueError, match=r".+"):
        function([{"product": " ", "units": 1, "unit_price": 3.0}])


def check_incident_triage(function: LogFunction) -> None:
    lines = [
        "2026-08-04T09:00:00Z INFO checkout complete",
        "2026-08-04T09:01:12Z ERROR payments provider timeout",
        "bad line",
        "",
        "2026-08-04T09:05:10Z CRITICAL checkout database unavailable",
    ]
    assert function(lines) == {
        "incidents": [
            {
                "timestamp": "2026-08-04T09:01:12Z",
                "level": "ERROR",
                "service": "payments",
                "message": "provider timeout",
            },
            {
                "timestamp": "2026-08-04T09:05:10Z",
                "level": "CRITICAL",
                "service": "checkout",
                "message": "database unavailable",
            },
        ],
        "invalid_lines": 1,
    }
    assert function([]) == {"incidents": [], "invalid_lines": 0}


def check_customer_features(function: FeatureFunction) -> None:
    events = pd.DataFrame(
        {
            "customer_id": ["c2", "c1", "c1", "c2", "c3"],
            "event": ["support", "purchase", "support", "purchase", "visit"],
            "amount": [0.0, 10.0, 0.0, 7.5, 0.0],
            "occurred_at": [
                "2026-01-01T09:00:00Z",
                "2026-01-01T10:00:00Z",
                "2026-01-03T10:00:00Z",
                "2026-01-02T09:00:00Z",
                "2026-01-04T12:00:00Z",
            ],
        }
    )
    original = events.copy(deep=True)
    actual = function(events)
    expected = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c3"],
            "purchase_count": [1, 1, 0],
            "total_spend": [10.0, 7.5, 0.0],
            "support_tickets": [1, 1, 0],
            "last_event_at": pd.to_datetime(
                [
                    "2026-01-03T10:00:00Z",
                    "2026-01-02T09:00:00Z",
                    "2026-01-04T12:00:00Z",
                ],
                utc=True,
            ),
        }
    )
    assert_frame_equal(actual, expected, check_dtype=False)
    assert_frame_equal(events, original)
    with pytest.raises(ValueError, match="missing"):
        function(events.drop(columns="amount"))


def check_classification_metrics(function: MetricFunction) -> None:
    actual = function([1, 1, 1, 0, 0, 0], [1, 0, 1, 0, 1, 0])
    assert actual["accuracy"] == pytest.approx(4 / 6)
    assert actual["precision"] == pytest.approx(2 / 3)
    assert actual["recall"] == pytest.approx(2 / 3)
    assert actual["f1"] == pytest.approx(2 / 3)
    assert actual["confusion_matrix"] == [[2, 1], [1, 2]]
    no_positive_predictions = function([0, 1], [0, 0])
    assert no_positive_predictions["precision"] == 0.0
    assert no_positive_predictions["f1"] == 0.0
    with pytest.raises(ValueError, match=r".+"):
        function([], [])
    with pytest.raises(ValueError, match=r".+"):
        function([0, 1], [0])


def check_risk_pipeline(function: PipelineFunction) -> None:
    random = np.random.default_rng(42)
    rows = 160
    frame = pd.DataFrame(
        {
            "age": random.integers(18, 75, rows).astype(float),
            "monthly_spend": random.normal(55, 18, rows),
            "country": random.choice(["BR", "US", "DE"], rows),
            "plan": random.choice(["free", "pro"], rows),
        }
    )
    target = ((frame["monthly_spend"] + 25 * (frame["plan"] == "pro")) > 62).astype(int)
    frame.loc[[3, 11], "monthly_spend"] = np.nan
    frame.loc[[5], "country"] = None
    original = frame.copy(deep=True)

    pipeline = function(seed=42)
    assert isinstance(pipeline, Pipeline)
    assert list(pipeline.named_steps) == ["preprocess", "model"]
    assert isinstance(pipeline.named_steps["preprocess"], ColumnTransformer)
    assert not hasattr(pipeline.named_steps["model"], "classes_")
    pipeline.fit(frame.iloc[:120], target.iloc[:120])
    assert pipeline.score(frame.iloc[120:], target.iloc[120:]) >= 0.8
    assert (
        len(
            pipeline.predict(
                pd.DataFrame([{"age": 40, "monthly_spend": 70.0, "country": "NEW", "plan": "pro"}])
            )
        )
        == 1
    )
    assert_frame_equal(frame, original)


def check_recommender(function: RecommendFunction) -> None:
    interactions = [
        ("u1", "a"),
        ("u1", "b"),
        ("u2", "a"),
        ("u2", "c"),
        ("u3", "a"),
        ("u3", "c"),
        ("u3", "d"),
        ("u4", "c"),
        ("u4", "d"),
    ]
    assert function(interactions, user_id="u1", k=2) == ["c", "d"]
    assert function(interactions, user_id="new", k=3) == ["a", "c", "d"]
    assert function(interactions, user_id="u1", k=99) == ["c", "d"]
    with pytest.raises(ValueError, match=r".+"):
        function(interactions, user_id="u1", k=0)


def check_job_batches(function: JobBatchFunction) -> None:
    jobs = [
        {"id": " job-1 ", "status": " QUEUED "},
        {"id": "job-2", "status": "running"},
        {"id": "job-3", "status": "succeeded"},
    ]
    original = [job.copy() for job in jobs]
    assert function(jobs, batch_size=2) == {
        "batches": [
            [
                {"id": "job-1", "status": "queued"},
                {"id": "job-2", "status": "running"},
            ],
            [{"id": "job-3", "status": "succeeded"}],
        ],
        "status_counts": {"queued": 1, "running": 1, "succeeded": 1, "failed": 0},
    }
    assert jobs == original
    assert function([], batch_size=3) == {
        "batches": [],
        "status_counts": {"queued": 0, "running": 0, "succeeded": 0, "failed": 0},
    }
    with pytest.raises(ValueError, match="batch_size"):
        function(jobs, batch_size=0)
    with pytest.raises(ValueError, match="duplicate"):
        function(
            [{"id": "same", "status": "queued"}, {"id": " same ", "status": "failed"}],
            batch_size=1,
        )
    with pytest.raises(ValueError, match="unknown status"):
        function([{"id": "job", "status": "waiting"}], batch_size=1)
    for invalid in (
        {"id": " ", "status": "queued"},
        {"id": "job"},
        {"id": "job", "status": "queued", "owner": "u1"},
    ):
        with pytest.raises(ValueError, match=r".+"):
            function([invalid], batch_size=1)


def check_training_config(function: TrainingConfigFunction) -> None:
    payload: dict[str, object] = {
        "model_name": " Tiny MLP ",
        "learning_rate": 0.01,
        "epochs": 8,
    }
    original = payload.copy()
    assert function(payload) == {
        "model_name": "tiny-mlp",
        "learning_rate": 0.01,
        "epochs": 8,
        "seed": 42,
    }
    assert payload == original
    assert function({**payload, "seed": 7})["seed"] == 7

    invalid_payloads = [
        {},
        {**payload, "owner": "team"},
        {**payload, "model_name": " "},
        {**payload, "learning_rate": 1},
        {**payload, "learning_rate": True},
        {**payload, "learning_rate": float("nan")},
        {**payload, "epochs": True},
        {**payload, "epochs": 0},
        {**payload, "seed": -1},
        {**payload, "seed": False},
    ]
    for invalid in invalid_payloads:
        with pytest.raises(ValidationError):
            function(invalid)


def check_missing_values(function: MissingValueFunction) -> None:
    frame = pd.DataFrame(
        {
            "country": ["BR", None, "US", None],
            "age": [31.0, 44.0, np.nan, 27.0],
            "plan": ["pro", "free", "pro", "free"],
        },
        index=[10, 11, 12, 13],
    )
    original = frame.copy(deep=True)
    expected = pd.DataFrame(
        {
            "column": ["country", "age", "plan"],
            "missing_count": [2, 1, 0],
            "missing_rate": [0.5, 0.25, 0.0],
        }
    )
    assert_frame_equal(function(frame), expected, check_dtype=False)
    assert_frame_equal(frame, original)

    empty_rows = pd.DataFrame(
        {
            "zeta": pd.Series(dtype="float64"),
            "alpha": pd.Series(dtype="object"),
        }
    )
    empty_summary = function(empty_rows)
    assert empty_summary.to_dict(orient="records") == [
        {"column": "alpha", "missing_count": 0, "missing_rate": 0.0},
        {"column": "zeta", "missing_count": 0, "missing_rate": 0.0},
    ]
    assert np.isfinite(empty_summary["missing_rate"]).all()

    with pytest.raises(ValueError, match="columns"):
        function(pd.DataFrame())
    with pytest.raises(ValueError, match="columns"):
        function(pd.DataFrame([[1, 2]], columns=["same", "same"]))
    with pytest.raises(ValueError, match="columns"):
        function(pd.DataFrame({1: ["value"]}))


def check_threshold_selection(function: ThresholdFunction) -> None:
    labels = [1, 0, 1, 0, 1]
    probabilities = [0.9, 0.8, 0.7, 0.6, 0.4]
    original_labels = labels.copy()
    original_probabilities = probabilities.copy()
    actual = function(labels, probabilities, 2 / 3)
    assert set(actual) == {"threshold", "precision", "recall", "predicted_positive"}
    assert actual["threshold"] == pytest.approx(0.7)
    assert actual["precision"] == pytest.approx(2 / 3)
    assert actual["recall"] == pytest.approx(2 / 3)
    assert actual["predicted_positive"] == 3
    assert labels == original_labels
    assert probabilities == original_probabilities

    precision_tie = function([1, 1, 0], [0.9, 0.8, 0.1], 0.5)
    assert precision_tie == {
        "threshold": 0.9,
        "precision": 1.0,
        "recall": 0.5,
        "predicted_positive": 1,
    }
    full_recall = function([1, 0, 1], [0.9, 0.5, 0.2], 1.0)
    assert full_recall["threshold"] == pytest.approx(0.2)
    assert full_recall["recall"] == 1.0

    invalid_calls: list[tuple[Sequence[object], Sequence[object], object]] = [
        ([], [], 0.5),
        ([1], [0.8, 0.7], 0.5),
        ([1, 2], [0.8, 0.7], 0.5),
        ([True], [0.8], 0.5),
        ([1], [True], 0.5),
        ([1], [-0.1], 0.5),
        ([1], [1.1], 0.5),
        ([1], [float("nan")], 0.5),
        ([1], [float("inf")], 0.5),
        ([1], [0.8], 0.0),
        ([1], [0.8], 1.1),
        ([1], [0.8], float("nan")),
        ([1], [0.8], True),
        ([0, 0], [0.8, 0.2], 0.5),
    ]
    for invalid_labels, invalid_probabilities, invalid_recall in invalid_calls:
        with pytest.raises(ValueError, match=r".+"):
            function(invalid_labels, invalid_probabilities, invalid_recall)  # type: ignore[arg-type]


def check_tensor_batches(function: TensorBatchFunction) -> None:
    features = np.array(
        [[0.1, 10.0], [0.2, 20.0], [0.3, 30.0], [0.4, 40.0], [0.5, 50.0]],
        dtype=np.float64,
    )
    labels = np.array([0, 1, 0, 1, 2], dtype=np.int32)
    original_features = features.copy()
    original_labels = labels.copy()

    batches = function(features, labels, batch_size=2, seed=7)
    assert [len(feature_batch) for feature_batch, _ in batches] == [2, 2, 1]
    combined_features = np.concatenate([feature_batch for feature_batch, _ in batches])
    combined_labels = np.concatenate([label_batch for _, label_batch in batches])
    expected_order = np.random.default_rng(7).permutation(len(features))
    np.testing.assert_array_equal(combined_features, features[expected_order].astype(np.float32))
    np.testing.assert_array_equal(combined_labels, labels[expected_order].astype(np.int64))
    assert combined_features.dtype == np.float32
    assert combined_labels.dtype == np.int64
    for feature_batch, label_batch in batches:
        assert not np.shares_memory(feature_batch, features)
        assert not np.shares_memory(label_batch, labels)

    repeated = function(features, labels, batch_size=2, seed=7)
    for first, second in zip(batches, repeated, strict=True):
        np.testing.assert_array_equal(first[0], second[0])
        np.testing.assert_array_equal(first[1], second[1])
    np.testing.assert_array_equal(features, original_features)
    np.testing.assert_array_equal(labels, original_labels)
    assert function(np.empty((0, 3)), np.array([], dtype=np.int64), batch_size=4, seed=0) == []

    invalid_calls = [
        ([1.0, 2.0], [0, 1], 1, 0),
        (np.empty((2, 0)), [0, 1], 1, 0),
        ([[1.0], [2.0]], [0], 1, 0),
        ([[1.0], [float("nan")]], [0, 1], 1, 0),
        ([[1.0], [float("inf")]], [0, 1], 1, 0),
        ([["one"]], [0], 1, 0),
        (np.array([[1 + 2j]]), [0], 1, 0),
        ([[1.0], [2.0]], np.array([0.0, 1.0]), 1, 0),
        ([[1.0]], np.array([True]), 1, 0),
        ([[1.0]], np.array([-1]), 1, 0),
        ([[1.0]], np.array([0]), 0, 0),
        ([[1.0]], np.array([0]), True, 0),
        ([[1.0]], np.array([0]), 1, -1),
        ([[1.0]], np.array([0]), 1, True),
    ]
    for invalid_features, invalid_labels, invalid_batch_size, invalid_seed in invalid_calls:
        with pytest.raises(ValueError, match=r".+"):
            function(
                invalid_features,
                invalid_labels,
                batch_size=invalid_batch_size,
                seed=invalid_seed,
            )


def check_prediction_envelope(function: PredictionEnvelopeFunction) -> None:
    predictions: list[dict[str, object]] = [
        {"item_id": " row-2 ", "label": " review ", "confidence": 0.82},
        {"item_id": "row-1", "label": "safe", "confidence": 0.73},
        {"item_id": "row-3", "label": "review", "confidence": 0.61},
    ]
    original = deepcopy(predictions)
    actual = function(predictions, request_id=" req-7 ", model_version=" risk-v3 ")
    assert actual == {
        "request_id": "req-7",
        "model_version": "risk-v3",
        "predictions": [
            {"item_id": "row-2", "label": "review", "confidence": 0.82},
            {"item_id": "row-1", "label": "safe", "confidence": 0.73},
            {"item_id": "row-3", "label": "review", "confidence": 0.61},
        ],
        "label_counts": {"review": 2, "safe": 1},
    }
    assert list(actual) == ["request_id", "model_version", "predictions", "label_counts"]
    assert list(actual["label_counts"]) == ["review", "safe"]  # type: ignore[arg-type]
    assert predictions == original
    assert function([], request_id="empty", model_version="model-v1") == {
        "request_id": "empty",
        "model_version": "model-v1",
        "predictions": [],
        "label_counts": {},
    }

    valid = {"item_id": "row", "label": "safe", "confidence": 0.5}
    invalid_calls: list[tuple[list[dict[str, object]], object, object]] = [
        ([{**valid, "item_id": f"row-{index}"} for index in range(101)], "req", "v1"),
        ([valid, {**valid, "item_id": " row "}], "req", "v1"),
        ([{"item_id": "row", "label": "safe"}], "req", "v1"),
        ([{**valid, "owner": "team"}], "req", "v1"),
        ([{**valid, "item_id": " "}], "req", "v1"),
        ([{**valid, "label": " "}], "req", "v1"),
        ([{**valid, "confidence": 1}], "req", "v1"),
        ([{**valid, "confidence": True}], "req", "v1"),
        ([{**valid, "confidence": "0.5"}], "req", "v1"),
        ([{**valid, "confidence": -0.1}], "req", "v1"),
        ([{**valid, "confidence": 1.1}], "req", "v1"),
        ([{**valid, "confidence": float("nan")}], "req", "v1"),
        ([{**valid, "confidence": float("inf")}], "req", "v1"),
        ([valid], " ", "v1"),
        ([valid], 7, "v1"),
        ([valid], "req", " "),
    ]
    for invalid_predictions, invalid_request_id, invalid_model_version in invalid_calls:
        with pytest.raises(ValidationError):
            function(
                invalid_predictions,
                request_id=invalid_request_id,
                model_version=invalid_model_version,
            )


def callable_from(module: Any, name: str) -> Callable[..., Any]:
    value = getattr(module, name)
    assert callable(value), f"{name} must be callable"
    return value
