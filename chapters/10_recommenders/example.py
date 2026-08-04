"""Recommend globally popular unseen items and evaluate the ranking."""

import csv
from datetime import UTC, datetime
from pathlib import Path

from learn_python_quick.recommender import (
    Interaction,
    evaluate_recommendations,
    recommend_popular_unseen,
    temporal_user_split,
)


def load_interactions() -> list[Interaction]:
    root = Path(__file__).resolve().parents[2]
    with (root / "datasets/generated/interactions.csv").open(encoding="utf-8") as stream:
        return [
            Interaction(
                row["user_id"],
                row["item_id"],
                float(row["rating"]),
                datetime.fromisoformat(row["occurred_at"]),
            )
            for row in csv.DictReader(stream)
        ]


def main() -> None:
    cutoff = datetime(2026, 7, 10, tzinfo=UTC)
    training, relevant = temporal_user_split(load_interactions(), cutoff=cutoff, user_id="u1")
    recommendations = recommend_popular_unseen(training, user_id="u1", k=2)
    print(f"cutoff={cutoff.isoformat()} training_rows={len(training)}")
    print(f"u1 future unseen={sorted(relevant)}")
    print(f"u1 recommendations={recommendations}")
    print(evaluate_recommendations(recommendations, relevant, k=2))


if __name__ == "__main__":
    main()
