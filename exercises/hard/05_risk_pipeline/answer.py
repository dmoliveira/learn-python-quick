"""Learner answer for the leakage-safe risk pipeline exercise."""

from __future__ import annotations

from sklearn.pipeline import Pipeline


def build_risk_pipeline(*, seed: int = 42) -> Pipeline:
    """Return an unfitted mixed-feature preprocessing and classification pipeline."""
    raise NotImplementedError("Implement build_risk_pipeline using the exercise contract")
