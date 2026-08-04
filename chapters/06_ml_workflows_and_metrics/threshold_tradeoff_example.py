"""Compare decision thresholds on one fixed validation set."""

from collections.abc import Sequence

from sklearn.metrics import precision_score, recall_score


def report_threshold(
    labels: Sequence[int],
    scores: Sequence[float],
    threshold: float,
) -> dict[str, float | int]:
    predictions = [int(score >= threshold) for score in scores]
    return {
        "threshold": threshold,
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "reviews": sum(predictions),
    }


def main() -> None:
    validation_labels = [1, 0, 1, 0, 1, 0, 0, 1]
    validation_scores = [0.91, 0.82, 0.76, 0.64, 0.58, 0.46, 0.31, 0.22]

    for threshold in (0.3, 0.5, 0.7):
        result = report_threshold(validation_labels, validation_scores, threshold)
        print(
            f"threshold={result['threshold']:.1f} reviews={result['reviews']} "
            f"precision={result['precision']:.2f} recall={result['recall']:.2f}"
        )


if __name__ == "__main__":
    main()
