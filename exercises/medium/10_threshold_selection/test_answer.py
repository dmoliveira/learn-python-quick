from tests.contracts import callable_from, check_threshold_selection
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_threshold_selection(callable_from(answer, "select_decision_threshold"))
