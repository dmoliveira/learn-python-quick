"""Optional FastAPI prediction boundary with typed requests and responses."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from functools import lru_cache
from typing import Any, Protocol, TypeVar, cast

from pydantic import BaseModel, ConfigDict, Field
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from learn_python_quick.optional import require_module

F = TypeVar("F", bound=Callable[..., object])


class AppLike(Protocol):
    """The small decorator surface used from a dynamically imported FastAPI app."""

    def get(self, path: str) -> Callable[[F], F]: ...

    def post(self, path: str, *, response_model: type[BaseModel]) -> Callable[[F], F]: ...


class PredictionRequest(BaseModel):
    """Four measurements expected by the Iris teaching model."""

    model_config = ConfigDict(extra="forbid")
    features: tuple[float, float, float, float] = Field(
        description="Sepal length/width, then petal length/width in centimeters"
    )


class PredictionResponse(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)
    model_version: str


class BatchPredictionRequest(BaseModel):
    """A bounded group of rows for one in-process model call."""

    model_config = ConfigDict(extra="forbid")
    rows: list[PredictionRequest] = Field(min_length=1, max_length=100)


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


@lru_cache(maxsize=1)
def _model() -> tuple[Pipeline, tuple[str, ...]]:
    dataset = load_iris()
    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=500, random_state=42)),
        ]
    )
    model.fit(dataset.data, dataset.target)
    return model, tuple(str(name) for name in dataset.target_names)


def create_app() -> AppLike:
    """Create an app lazily so the core package does not require FastAPI."""
    fastapi: Any = require_module("fastapi", extra="api")
    app = cast(
        AppLike,
        fastapi.FastAPI(
            title="Learn Python Quick prediction API",
            version="0.1.0",
            description="An educational in-process model serving example.",
        ),
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "model_version": "iris-logistic-v1"}

    @app.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest) -> PredictionResponse:
        return _predict_one(payload)

    @app.post("/predict-batch", response_model=BatchPredictionResponse)
    def predict_batch(payload: BatchPredictionRequest) -> BatchPredictionResponse:
        return BatchPredictionResponse(
            predictions=_predict_many(payload.rows),
        )

    return app


def _predict_one(payload: PredictionRequest) -> PredictionResponse:
    return _predict_many([payload])[0]


def _predict_many(payloads: Sequence[PredictionRequest]) -> list[PredictionResponse]:
    model, labels = _model()
    probability_rows = model.predict_proba([payload.features for payload in payloads])
    responses: list[PredictionResponse] = []
    for probabilities in probability_rows:
        label_index = int(probabilities.argmax())
        responses.append(
            PredictionResponse(
                label=labels[label_index],
                confidence=float(probabilities[label_index]),
                model_version="iris-logistic-v1",
            )
        )
    return responses
