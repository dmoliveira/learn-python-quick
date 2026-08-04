from tests.contracts import callable_from, check_missing_values
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_missing_values(callable_from(answer, "summarize_missing_values"))
