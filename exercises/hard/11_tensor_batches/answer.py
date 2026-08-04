"""Learner answer for the deterministic tensor-batch exercise."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def prepare_training_batches(
    features: ArrayLike,
    labels: ArrayLike,
    batch_size: int,
    seed: int = 42,
) -> list[tuple[NDArray[np.float32], NDArray[np.int64]]]:
    """Validate, align, shuffle, and batch training arrays."""
    raise NotImplementedError("Implement prepare_training_batches using the exercise contract")
