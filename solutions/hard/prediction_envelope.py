"""Solution: validate a bounded prediction response and derive stable counts."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator


def _strict_non_blank_text(value: object, *, name: str) -> str:
    if type(value) is not str:
        raise ValueError(f"{name} must be a strict string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must not be blank")
    return normalized


class _Prediction(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    item_id: str
    label: str
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("item_id", "label", mode="before")
    @classmethod
    def validate_text(cls, value: object, info: ValidationInfo) -> str:
        return _strict_non_blank_text(value, name=info.field_name)

    @field_validator("confidence", mode="before")
    @classmethod
    def validate_confidence(cls, value: object) -> float:
        if type(value) is not float or not math.isfinite(value):
            raise ValueError("confidence must be a finite Python float")
        return value


class _Envelope(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    request_id: str
    model_version: str
    predictions: list[_Prediction] = Field(max_length=100)

    @field_validator("request_id", "model_version", mode="before")
    @classmethod
    def validate_text(cls, value: object, info: ValidationInfo) -> str:
        return _strict_non_blank_text(value, name=info.field_name)

    @model_validator(mode="after")
    def validate_unique_item_ids(self) -> Self:
        item_ids = [prediction.item_id for prediction in self.predictions]
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("prediction item_id values must be unique")
        return self


def build_prediction_envelope(
    predictions: Sequence[Mapping[str, object]],
    request_id: str,
    model_version: str,
) -> dict[str, object]:
    envelope = _Envelope.model_validate(
        {
            "request_id": request_id,
            "model_version": model_version,
            "predictions": list(predictions),
        }
    )
    prediction_rows = [prediction.model_dump() for prediction in envelope.predictions]
    counts = Counter(prediction.label for prediction in envelope.predictions)
    return {
        "request_id": envelope.request_id,
        "model_version": envelope.model_version,
        "predictions": prediction_rows,
        "label_counts": dict(sorted(counts.items())),
    }
