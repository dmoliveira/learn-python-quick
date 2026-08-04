"""Solution: rank popular unseen items with explicit deterministic ties."""

from __future__ import annotations

from collections import Counter


def recommend_unseen(
    interactions: list[tuple[str, str]],
    *,
    user_id: str,
    k: int,
) -> list[str]:
    if k < 1:
        raise ValueError("k must be at least 1")
    popularity = Counter(item for _, item in interactions)
    seen = {item for user, item in interactions if user == user_id}
    candidates = (item for item in popularity if item not in seen)
    return sorted(candidates, key=lambda item: (-popularity[item], item))[:k]
