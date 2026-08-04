from tests.contracts import callable_from, check_recommender
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_recommender(callable_from(answer, "recommend_unseen"))
