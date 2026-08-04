from __future__ import annotations

import pytest
from pydantic import ValidationError

from learn_python_quick.foundations import (
    JobStatus,
    SaleRow,
    batched,
    format_metric,
    next_action,
    safe_divide,
    summarize_sales,
)
from learn_python_quick.models import (
    InvalidFeaturesError,
    ThresholdPredictor,
    TrainingConfig,
    describe_prediction,
)


def test_summarize_sales_handles_ties_and_generators() -> None:
    rows: list[SaleRow] = [
        {"product": " zed ", "units": 2, "unit_price": 1.25},
        {"product": "alpha", "units": 2, "unit_price": 2.0},
    ]
    result = summarize_sales(iter(rows))
    assert result.revenue == 6.5
    assert result.units_by_product == {"alpha": 2, "zed": 2}
    assert result.best_seller == "alpha"


@pytest.mark.parametrize(
    "row",
    [
        {"product": "", "units": 1, "unit_price": 1.0},
        {"product": "tea", "units": -1, "unit_price": 1.0},
        {"product": "tea", "units": 1, "unit_price": -1.0},
    ],
)
def test_summarize_sales_rejects_invalid_values(row: SaleRow) -> None:
    with pytest.raises(ValueError, match=r".+"):
        summarize_sales([row])


def test_function_argument_and_iteration_examples() -> None:
    assert list(batched(range(5), 2)) == [(0, 1), (2, 3), (4,)]
    with pytest.raises(ValueError, match="size"):
        list(batched([], 0))
    assert safe_divide(2, 0, default=-1) == -1
    assert format_metric("f1", 0.876, digits=2) == "f1: 0.88"
    assert next_action(JobStatus.FAILED) == "inspect logs"


def test_pydantic_config_normalizes_and_rejects_extra_fields() -> None:
    config = TrainingConfig(model_name=" Tiny Model ", learning_rate=0.1, epochs=2)
    assert config.model_name == "tiny-model"
    with pytest.raises(ValidationError):
        TrainingConfig(model_name="x", learning_rate=0.1, epochs=2, unknown=True)  # type: ignore[call-arg]


def test_protocol_based_predictor() -> None:
    predictor = ThresholdPredictor(threshold=0.5)
    assert describe_prediction(predictor, [0.2, 0.8]) == "positive (50.00%)"
    with pytest.raises(InvalidFeaturesError):
        predictor.predict_one([])
