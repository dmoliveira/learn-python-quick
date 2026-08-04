from solutions.easy.incident_log import triage_incidents
from solutions.easy.sales_summary import summarize_sales
from solutions.hard.recommender import recommend_unseen
from solutions.hard.risk_pipeline import build_risk_pipeline
from solutions.medium.classification_metrics import evaluate_binary_classifier
from solutions.medium.customer_features import build_customer_features
from tests.contracts import (
    check_classification_metrics,
    check_customer_features,
    check_incident_triage,
    check_recommender,
    check_risk_pipeline,
    check_sales_summary,
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
