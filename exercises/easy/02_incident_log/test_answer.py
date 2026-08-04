from tests.contracts import callable_from, check_incident_triage
from tests.learner import load_answer


def test_public_contract() -> None:
    answer = load_answer(__file__)
    check_incident_triage(callable_from(answer, "triage_incidents"))
