from __future__ import annotations

import numpy as np
import pytest

from learn_python_quick.data import (
    load_digit_images,
    load_medical_classification,
    load_regression_data,
    load_wine_frame,
    medical_train_test_split,
)
from learn_python_quick.ml import (
    build_logistic_pipeline,
    compare_tree_models,
    train_diabetes_regression,
    train_medical_classifier,
)


def test_packaged_datasets_have_expected_shapes() -> None:
    medical_x, medical_y = load_medical_classification()
    regression_x, regression_y = load_regression_data()
    digits_x, digits_y = load_digit_images()
    assert medical_x.shape == (569, 30)
    assert len(medical_y) == 569
    assert regression_x.shape == (442, 10)
    assert len(regression_y) == 442
    assert digits_x.shape == (1797, 64)
    assert len(digits_y) == 1797
    assert {"target", "class_name"}.issubset(load_wine_frame().columns)


def test_split_is_stratified_and_validates_size() -> None:
    split = medical_train_test_split(seed=42)
    assert len(split.x_train) + len(split.x_test) == 569
    assert abs(float(split.y_train.mean()) - float(split.y_test.mean())) < 0.03
    with pytest.raises(ValueError, match="test_size"):
        medical_train_test_split(test_size=1.0)


def test_classification_pipeline_is_repeatable_and_strong_enough() -> None:
    first = train_medical_classifier(seed=42)
    second = train_medical_classifier(seed=42)
    assert first.metrics == pytest.approx(second.metrics)
    assert first.metrics["f1"] > 0.9
    assert first.metrics["roc_auc"] > 0.95
    assert list(build_logistic_pipeline().named_steps) == ["scale", "model"]


def test_tree_and_regression_baselines_report_bounded_metrics() -> None:
    trees = compare_tree_models(seed=42)
    assert all(0.8 < value <= 1.0 for value in trees.values())
    regression = train_diabetes_regression(alpha=1.0)
    assert 30 < regression.metrics["mae"] < 60
    assert np.isfinite(list(regression.metrics.values())).all()
