from tests.contracts import callable_from, check_customer_features
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_customer_features(callable_from(answer, "build_customer_features"))
