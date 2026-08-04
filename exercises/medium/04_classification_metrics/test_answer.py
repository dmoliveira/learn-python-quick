from tests.contracts import callable_from, check_classification_metrics
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_classification_metrics(callable_from(answer, "evaluate_binary_classifier"))
