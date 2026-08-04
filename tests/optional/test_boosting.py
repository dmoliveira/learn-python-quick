import pytest

from learn_python_quick.boosting import train_xgboost_classifier

pytestmark = pytest.mark.boost


def test_xgboost_training_is_bounded_and_useful() -> None:
    run = train_xgboost_classifier(seed=42, max_rounds=30)
    assert run.train_rows + run.validation_rows + run.test_rows == 569
    assert run.validation_rows > 0
    assert run.test_rows > 0
    assert 1 <= run.rounds_used <= 30
    assert run.metrics["f1"] > 0.85
    assert run.metrics["roc_auc"] > 0.9
