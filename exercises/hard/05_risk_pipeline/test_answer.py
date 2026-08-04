from tests.contracts import callable_from, check_risk_pipeline
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_risk_pipeline(callable_from(answer, "build_risk_pipeline"))
