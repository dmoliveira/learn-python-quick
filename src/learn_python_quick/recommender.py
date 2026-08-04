"""Transparent recommendation baselines and ranking evaluation."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta

from learn_python_quick.evaluation import precision_at_k, recall_at_k


@dataclass(frozen=True, slots=True)
class Interaction:
    user_id: str
    item_id: str
    rating: float = 1.0
    occurred_at: datetime | None = None


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


def temporal_user_split(
    interactions: Iterable[Interaction],
    *,
    cutoff: datetime,
    user_id: str,
) -> tuple[list[Interaction], set[str]]:
    """Return pre-cutoff rows and future unseen items available as training candidates."""
    _validate_utc(cutoff, name="cutoff")
    training: list[Interaction] = []
    training_candidates: set[str] = set()
    seen_before_cutoff: set[str] = set()
    future_positive: set[str] = set()

    for interaction in interactions:
        timestamp = interaction.occurred_at
        if timestamp is None:
            raise ValueError("every interaction needs occurred_at")
        _validate_utc(timestamp, name="occurred_at")
        if timestamp < cutoff:
            training.append(interaction)
            if interaction.rating > 0:
                training_candidates.add(interaction.item_id)
            if interaction.user_id == user_id:
                seen_before_cutoff.add(interaction.item_id)
        elif interaction.user_id == user_id and interaction.rating > 0:
            future_positive.add(interaction.item_id)

    relevant = (future_positive - seen_before_cutoff) & training_candidates
    return training, relevant


def _validate_utc(value: datetime, *, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware UTC")
    if value.utcoffset() != timedelta(0):
        raise ValueError(f"{name} must use UTC")
