"""Transparent recommendation baselines and ranking evaluation."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

from learn_python_quick.evaluation import precision_at_k, recall_at_k


@dataclass(frozen=True, slots=True)
class Interaction:
    user_id: str
    item_id: str
    rating: float = 1.0


def recommend_popular_unseen(
    interactions: Iterable[Interaction],
    *,
    user_id: str,
    k: int = 3,
) -> list[str]:
    """Rank globally popular items while excluding the user's seen items."""
    if k < 1:
        raise ValueError("k must be at least 1")
    rows = list(interactions)
    seen = {row.item_id for row in rows if row.user_id == user_id}
    popularity = Counter(row.item_id for row in rows if row.rating > 0)
    candidates = (item for item in popularity if item not in seen)
    return sorted(candidates, key=lambda item: (-popularity[item], item))[:k]


def evaluate_recommendations(
    recommended: list[str],
    relevant: set[str],
    *,
    k: int,
) -> dict[str, float]:
    """Keep metric definitions next to an explicit cutoff."""
    return {
        f"precision@{k}": precision_at_k(recommended, relevant, k=k),
        f"recall@{k}": recall_at_k(recommended, relevant, k=k),
    }
