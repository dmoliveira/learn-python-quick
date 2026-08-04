"""Small, offline dataset helpers used across the course."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import pandas as pd
from sklearn.datasets import load_breast_cancer, load_diabetes, load_digits, load_wine
from sklearn.model_selection import train_test_split


@dataclass(frozen=True, slots=True)
class TabularSplit:
    """A named train/test split makes accidental mixing easier to spot."""

    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def load_medical_classification() -> tuple[pd.DataFrame, pd.Series]:
    """Load the packaged Breast Cancer Wisconsin features and labels."""
    dataset = load_breast_cancer(as_frame=True)
    return cast(pd.DataFrame, dataset.data), cast(pd.Series, dataset.target)


def medical_train_test_split(*, seed: int = 42, test_size: float = 0.2) -> TabularSplit:
    """Create a stratified split before fitting any preprocessing."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    features, target = load_medical_classification()
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=seed,
        stratify=target,
    )
    return TabularSplit(x_train, x_test, y_train, y_test)


def load_regression_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load the packaged Diabetes regression dataset."""
    dataset = load_diabetes(as_frame=True)
    return cast(pd.DataFrame, dataset.data), cast(pd.Series, dataset.target)


def load_wine_frame() -> pd.DataFrame:
    """Return Wine features and a readable target column in one frame."""
    dataset = load_wine(as_frame=True)
    frame = cast(pd.DataFrame, dataset.frame).copy()
    frame["class_name"] = frame["target"].map(dict(enumerate(dataset.target_names)))
    return frame


def load_digit_images() -> tuple[pd.DataFrame, pd.Series]:
    """Return flattened 8-by-8 digit images; no network download is needed."""
    dataset = load_digits(as_frame=True)
    return cast(pd.DataFrame, dataset.data), cast(pd.Series, dataset.target)
