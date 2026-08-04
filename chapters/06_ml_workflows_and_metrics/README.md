# 06 · ML workflows and metrics 🎯

**Time:** 80 minutes · **Prerequisites:** [NumPy and pandas](../05_numpy_and_pandas/README.md)

## Outcomes

You will be able to:

- turn a product question into features, labels, a baseline, and a metric;
- separate train, validation, and test roles;
- prevent common forms of data leakage with pipelines;
- train regression and classification baselines;
- interpret MAE, RMSE, R², precision, recall, F1, and ROC-AUC.

## Start with the decision

Prediction is useful only when it changes an action. Write down:

1. **Unit:** what one row represents.
2. **Prediction time:** what information exists then.
3. **Label:** what future or observed outcome is learned.
4. **Action:** what happens after a prediction.
5. **Cost:** which mistakes matter most.

A baseline may be the mean, majority class, recent value, or a simple rule. If a complex model does
not beat it on the same split and metric, complexity has not earned its cost.

## Split before learning transformations

Scaling, imputation, feature selection, and target encoding learn from data. Put them inside a
scikit-learn `Pipeline`, fit on training data, tune with validation/cross-validation, and inspect the
test set once for a final estimate.

Random splits are wrong when time, users, groups, or duplicates can cross the boundary. Use temporal
or grouped splits when deployment will face future periods or unseen groups.

## Metrics are trade-offs

- Regression: report MAE for typical target-unit error and RMSE when large errors matter more.
- Classification: accuracy fits balanced equal-cost errors; precision and recall expose different
  costs; F1 balances them; ROC-AUC measures ranking, not threshold behavior.
- Probability decisions need calibration measures such as log loss or Brier score.

See the full [metrics field guide](../../docs/metrics.md). Always inspect errors and slices, not only
one aggregate number.

## Run it

```bash
uv run python chapters/06_ml_workflows_and_metrics/example.py
```

## Try it

- Change the classification threshold and compare precision with recall.
- Replace Ridge with a mean baseline and compare MAE.
- List three ways patient or customer records could leak across a random split.
- Solve [Evaluate a classifier](../../exercises/medium/04_classification_metrics/README.md).
- Later solve the [leakage-safe pipeline](../../exercises/hard/05_risk_pipeline/README.md).

## References

- [scikit-learn model selection](https://scikit-learn.org/stable/model_selection.html)
- [Pipelines](https://scikit-learn.org/stable/modules/compose.html#pipeline)
- [Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Common pitfalls and data leakage](https://scikit-learn.org/stable/common_pitfalls.html)
