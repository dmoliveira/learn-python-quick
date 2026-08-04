"""Validate untrusted input, then depend on a small predictor protocol."""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from learn_python_quick.models import Prediction, Predictor


class PredictionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: tuple[float, ...] = Field(min_length=1, max_length=8)


class FixedPredictor:
    """A test double that satisfies Predictor without inheritance."""

    def predict_one(self, features: Sequence[float]) -> Prediction:
        return Prediction(label="review", score=sum(features) / len(features))


def handle_prediction(payload: object, predictor: Predictor) -> dict[str, object]:
    request = PredictionPayload.model_validate(payload)
    prediction = predictor.predict_one(request.features)
    return {"label": prediction.label, "score": round(prediction.score, 3)}


def main() -> None:
    predictor = FixedPredictor()
    print(handle_prediction({"features": [0.2, 0.8]}, predictor))
    try:
        handle_prediction({"features": [], "extra": True}, predictor)
    except ValidationError as error:
        print(f"boundary rejected {error.error_count()} invalid field(s)")


if __name__ == "__main__":
    main()
