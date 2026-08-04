"""Train optional XGBoost with bounded rounds and early stopping."""

from learn_python_quick.boosting import train_xgboost_classifier


def main() -> None:
    run = train_xgboost_classifier(seed=42, max_rounds=50)
    print(
        f"rows={run.train_rows}/{run.validation_rows}/{run.test_rows} "
        f"rounds={run.rounds_used} f1={run.metrics['f1']:.3f} auc={run.metrics['roc_auc']:.3f}"
    )


if __name__ == "__main__":
    main()
