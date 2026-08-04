"""Classes, protocols, exceptions, and Pydantic v2 models."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InvalidFeaturesError(ValueError):
    """Raised when a predictor receives an unusable feature vector."""


class TrainingConfig(BaseModel):
    """Validate configuration at the system boundary, not deep in training."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    model_name: str = Field(min_length=1, max_length=80)
    learning_rate: float = Field(gt=0, le=1)
    epochs: int = Field(ge=1, le=10_000)
    seed: int = Field(default=42, ge=0)
    tags: tuple[str, ...] = ()

    @field_validator("model_name")
    @classmethod
    def normalize_model_name(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("model_name must contain visible characters")
        return normalized


@dataclass(frozen=True, slots=True)
class Prediction:
    label: str
    score: float


class Predictor(Protocol):
    """Structural contract: inheritance is not required."""

    def predict_one(self, features: Sequence[float]) -> Prediction: ...


@dataclass(frozen=True, slots=True)
class ThresholdPredictor:
    """Composition-friendly example implementation of ``Predictor``."""

    threshold: float = 0.5

    def predict_one(self, features: Sequence[float]) -> Prediction:
        if not features:
            raise InvalidFeaturesError("at least one feature is required")
        score = sum(features) / len(features)
        label = "positive" if score >= self.threshold else "negative"
        return Prediction(label=label, score=score)


def describe_prediction(predictor: Predictor, features: Sequence[float]) -> str:
    """Depend on the protocol instead of a concrete model class."""
    prediction = predictor.predict_one(features)
    return f"{prediction.label} ({prediction.score:.2%})"
