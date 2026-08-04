from tests.contracts import callable_from, check_prediction_envelope
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_prediction_envelope(callable_from(answer, "build_prediction_envelope"))
