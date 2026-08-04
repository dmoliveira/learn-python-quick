from tests.contracts import callable_from, check_tensor_batches
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_tensor_batches(callable_from(answer, "prepare_training_batches"))
