# 07 · Trees and XGBoost 🌲

**Time:** 60 minutes · **Prerequisites:** [ML workflows](../06_ml_workflows_and_metrics/README.md)

## Outcomes

You will be able to:

- explain how decision trees split the feature space;
- control depth and minimum samples to reduce overfitting;
- compare bagging/random forests with gradient boosting;
- train a small XGBoost classifier with early stopping;
- inspect importance carefully without turning it into causality.

## From one tree to an ensemble

A decision tree repeatedly chooses a feature threshold that improves node purity or reduces error.
Deep trees can memorize noise. Start with a shallow tree and compare train versus validation behavior.

Random forests train many decorrelated trees and average them. Gradient boosting trains each new tree
to correct current errors. XGBoost is an optimized boosting library with regularization, missing-value
handling, subsampling, and efficient histogram algorithms.

Important controls:

| Parameter | Effect |
|---|---|
| `max_depth` | interaction complexity per tree |
| `learning_rate` | contribution of each boosted tree |
| `n_estimators` | maximum boosting rounds |
| `subsample` / `colsample_bytree` | row/feature sampling and regularization |
| early stopping | stop when validation no longer improves |

Never use the final test set for early stopping. The course example splits training data again, uses
that validation part for early stopping, and evaluates on the untouched test part once. A real
workflow should also use cross-validation or repeated runs to quantify uncertainty.

Feature importance shows model usage, not causal effect. Correlated features can share or hide
importance. Check permutation importance and slice behavior before making claims.

## Run it

Core tree comparison:

```bash
uv run python chapters/07_trees_and_xgboost/example.py
```

Optional XGBoost run:

```bash
uv sync --dev --extra boost
uv run python chapters/07_trees_and_xgboost/xgboost_example.py
```

## Try it

- Compare tree depths 2, 4, and unlimited on train/test accuracy.
- Change one XGBoost regularization parameter at a time.
- Report run time and metric change; do not call a difference an improvement without uncertainty.
- Try [Tune boosted trees](../../docs/exercise-guide.md#challenge-catalog).

## References

- [scikit-learn decision trees](https://scikit-learn.org/stable/modules/tree.html)
- [Ensemble methods](https://scikit-learn.org/stable/modules/ensemble.html)
- [XGBoost Python API](https://xgboost.readthedocs.io/en/stable/python/python_api.html)
- [XGBoost parameter guide](https://xgboost.readthedocs.io/en/stable/parameter.html)
