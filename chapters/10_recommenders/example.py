"""Recommend globally popular unseen items and evaluate the ranking."""

import csv
from pathlib import Path

from learn_python_quick.recommender import (
    Interaction,
    evaluate_recommendations,
    recommend_popular_unseen,
)


def load_interactions() -> list[Interaction]:
    root = Path(__file__).resolve().parents[2]
    with (root / "datasets/generated/interactions.csv").open(encoding="utf-8") as stream:
        return [
            Interaction(row["user_id"], row["item_id"], float(row["rating"]))
            for row in csv.DictReader(stream)
        ]


def main() -> None:
    recommendations = recommend_popular_unseen(load_interactions(), user_id="u1", k=2)
    print(f"u1 recommendations={recommendations}")
    print(evaluate_recommendations(recommendations, {"data-course"}, k=2))


if __name__ == "__main__":
    main()
