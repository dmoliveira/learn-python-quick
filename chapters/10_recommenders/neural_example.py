"""Fit tiny optional user/item embeddings with PyTorch."""

import csv
from pathlib import Path

from learn_python_quick.deep_learning import train_neural_recommender
from learn_python_quick.recommender import Interaction


def load_interactions() -> list[Interaction]:
    root = Path(__file__).resolve().parents[2]
    with (root / "datasets/generated/interactions.csv").open(encoding="utf-8") as stream:
        return [
            Interaction(row["user_id"], row["item_id"], float(row["rating"]))
            for row in csv.DictReader(stream)
        ]


def main() -> None:
    recommendations = train_neural_recommender(
        load_interactions(),
        user_id="u1",
        k=2,
        seed=42,
        epochs=30,
    )
    print(f"neural recommendations for u1={recommendations}")


if __name__ == "__main__":
    main()
