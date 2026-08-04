"""Train one classification and one regression baseline."""

from learn_python_quick.ml import train_diabetes_regression, train_medical_classifier


def show_metrics(name: str, metrics: dict[str, float]) -> None:
    rendered = ", ".join(f"{key}={value:.3f}" for key, value in sorted(metrics.items()))
    print(f"{name}: {rendered}")


def main() -> None:
    classification = train_medical_classifier(seed=42)
    regression = train_diabetes_regression(alpha=1.0)
    show_metrics("classification", classification.metrics)
    show_metrics("regression", regression.metrics)
    print(f"classification rows={classification.train_rows}+{classification.test_rows}")


if __name__ == "__main__":
    main()
