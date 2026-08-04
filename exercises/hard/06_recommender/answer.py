"""Learner answer for the popularity recommender exercise."""

from __future__ import annotations


def recommend_unseen(
    interactions: list[tuple[str, str]],
    *,
    user_id: str,
    k: int,
) -> list[str]:
    """Rank popular items that the requested user has not seen."""
    raise NotImplementedError("Implement recommend_unseen using the exercise contract")
