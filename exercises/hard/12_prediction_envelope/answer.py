"""Learner answer for the strict prediction-envelope exercise."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def build_prediction_envelope(
    predictions: Sequence[Mapping[str, object]],
    request_id: str,
    model_version: str,
) -> dict[str, object]:
    """Validate prediction records and return a serializable envelope."""
    raise NotImplementedError("Implement build_prediction_envelope using the exercise contract")
