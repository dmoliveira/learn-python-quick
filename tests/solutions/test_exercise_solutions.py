from solutions.easy.incident_log import triage_incidents
from solutions.easy.job_batches import plan_job_batches
from solutions.easy.sales_summary import summarize_sales
from solutions.easy.training_config import validate_training_config
from solutions.hard.prediction_envelope import build_prediction_envelope
from solutions.hard.recommender import recommend_unseen
from solutions.hard.risk_pipeline import build_risk_pipeline
from solutions.hard.tensor_batches import prepare_training_batches
from solutions.medium.classification_metrics import evaluate_binary_classifier
from solutions.medium.customer_features import build_customer_features
from solutions.medium.missing_values import summarize_missing_values
from solutions.medium.threshold_selection import select_decision_threshold
from tests.contracts import (
    check_classification_metrics,
    check_customer_features,
    check_incident_triage,
    check_job_batches,
    check_missing_values,
    check_prediction_envelope,
    check_recommender,
    check_risk_pipeline,
    check_sales_summary,
    check_tensor_batches,
    check_threshold_selection,
    check_training_config,
)


def test_sales_summary_solution() -> None:
    check_sales_summary(summarize_sales)


def test_incident_log_solution() -> None:
    check_incident_triage(triage_incidents)


def test_customer_features_solution() -> None:
    check_customer_features(build_customer_features)


def test_classification_metrics_solution() -> None:
    check_classification_metrics(evaluate_binary_classifier)


def test_risk_pipeline_solution() -> None:
    check_risk_pipeline(build_risk_pipeline)


def test_recommender_solution() -> None:
    check_recommender(recommend_unseen)


def test_job_batches_solution() -> None:
    check_job_batches(plan_job_batches)


def test_training_config_solution() -> None:
    check_training_config(validate_training_config)


def test_missing_values_solution() -> None:
    check_missing_values(summarize_missing_values)


def test_threshold_selection_solution() -> None:
    check_threshold_selection(select_decision_threshold)


def test_tensor_batches_solution() -> None:
    check_tensor_batches(prepare_training_batches)


def test_prediction_envelope_solution() -> None:
    check_prediction_envelope(build_prediction_envelope)
