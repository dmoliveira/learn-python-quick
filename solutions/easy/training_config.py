"""Solution: strict Pydantic v2 validation at the training boundary."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictTrainingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    model_name: str = Field(min_length=1, max_length=80, strict=True)
    learning_rate: float = Field(gt=0, le=1, strict=True)
    epochs: int = Field(ge=1, le=10_000, strict=True)
    seed: int = Field(default=42, ge=0, strict=True)

    @field_validator("model_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("model_name must contain visible characters")
        return normalized

    @field_validator("learning_rate", mode="before")
    @classmethod
    def require_float(cls, value: Any) -> Any:
        if type(value) is not float:
            raise ValueError("learning_rate must be a float")
        return value


def validate_training_config(payload: Mapping[str, object]) -> dict[str, object]:
    return StrictTrainingConfig.model_validate(payload).model_dump()
