"""Readable performance examples: measure first, then vectorize or cache."""

from __future__ import annotations

import math
from collections.abc import Sequence
from functools import lru_cache

import numpy as np
from numpy.typing import ArrayLike, NDArray


def zscore_with_python(values: Sequence[float]) -> list[float]:
    """Readable loop baseline for comparison with a vectorized version."""
    if not values:
        return []
    mean = math.fsum(values) / len(values)
    variance = math.fsum((value - mean) ** 2 for value in values) / len(values)
    standard_deviation = math.sqrt(variance)
    if standard_deviation == 0:
        return [0.0] * len(values)
    return [(value - mean) / standard_deviation for value in values]


def zscore_with_numpy(values: ArrayLike) -> NDArray[np.float64]:
    """Vectorize numeric work after behavior is understood and measured."""
    array = np.asarray(values, dtype=np.float64)
    if array.size == 0:
        return array
    standard_deviation = float(array.std())
    if standard_deviation == 0:
        return np.zeros_like(array)
    return (array - array.mean()) / standard_deviation


@lru_cache(maxsize=128)
def fibonacci(number: int) -> int:
    """Show memoization on a pure function; iteration is better for large values."""
    if number < 0:
        raise ValueError("number must be non-negative")
    if number < 2:
        return number
    return fibonacci(number - 1) + fibonacci(number - 2)
