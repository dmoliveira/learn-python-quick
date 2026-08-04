"""Solution: validate aligned arrays, then shuffle and batch copied data."""

from __future__ import annotations

from numbers import Integral

import numpy as np
from numpy.typing import ArrayLike, NDArray


def prepare_training_batches(
    features: ArrayLike,
    labels: ArrayLike,
    batch_size: int,
    seed: int = 42,
) -> list[tuple[NDArray[np.float32], NDArray[np.int64]]]:
    if isinstance(batch_size, bool) or not isinstance(batch_size, Integral) or batch_size < 1:
        raise ValueError("batch_size must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, Integral) or seed < 0:
        raise ValueError("seed must be a non-negative integer")

    feature_values = np.asarray(features)
    label_values = np.asarray(labels)
    if feature_values.ndim != 2 or feature_values.shape[1] == 0:
        raise ValueError("features must be 2D with at least one column")
    if label_values.ndim != 1:
        raise ValueError("labels must be one-dimensional")
    if len(feature_values) != len(label_values):
        raise ValueError("features and labels must have equal row counts")
    if np.issubdtype(feature_values.dtype, np.bool_) or not np.issubdtype(
        feature_values.dtype, np.number
    ):
        raise ValueError("features must contain real numeric values")
    if np.iscomplexobj(feature_values):
        raise ValueError("features must contain real numeric values")
    if np.issubdtype(label_values.dtype, np.bool_) or not np.issubdtype(
        label_values.dtype, np.integer
    ):
        raise ValueError("labels must use a non-boolean integer dtype")

    with np.errstate(over="ignore", invalid="ignore"):
        feature_array = feature_values.astype(np.float32, copy=True)
    if not np.isfinite(feature_array).all():
        raise ValueError("features must contain finite float32 values")
    label_array = label_values.astype(np.int64, copy=True)
    if (label_array < 0).any():
        raise ValueError("labels must be non-negative")
    if len(feature_array) == 0:
        return []

    order = np.random.default_rng(int(seed)).permutation(len(feature_array))
    shuffled_features = feature_array[order]
    shuffled_labels = label_array[order]
    return [
        (
            shuffled_features[start : start + int(batch_size)].copy(),
            shuffled_labels[start : start + int(batch_size)].copy(),
        )
        for start in range(0, len(shuffled_features), int(batch_size))
    ]
