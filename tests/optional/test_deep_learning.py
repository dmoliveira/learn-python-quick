import pytest

from learn_python_quick.deep_learning import train_digits_mlp, train_neural_recommender
from learn_python_quick.recommender import Interaction

pytestmark = pytest.mark.deep


def test_digits_mlp_learns_on_cpu() -> None:
    run = train_digits_mlp(seed=42, epochs=6, hidden_units=32)
    assert run.final_loss < run.initial_loss
    assert run.accuracy > 0.7


def test_neural_recommender_excludes_seen_items() -> None:
    rows = [
        Interaction("u1", "a"),
        Interaction("u2", "a"),
        Interaction("u2", "b"),
        Interaction("u3", "b"),
        Interaction("u3", "c"),
    ]
    result = train_neural_recommender(rows, user_id="u1", k=2, epochs=10)
    assert "a" not in result
    assert set(result).issubset({"b", "c"})
