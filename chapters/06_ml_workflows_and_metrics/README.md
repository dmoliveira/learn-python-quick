# 06 · ML workflows and metrics 🎯

**Time:** 80 minutes · **Prerequisites:** [NumPy and pandas](../05_numpy_and_pandas/README.md)

## Outcomes

You will be able to:

- turn a product question into features, labels, a baseline, and a metric;
- separate train, validation, and test roles;
- prevent common forms of data leakage with pipelines;
- train regression and classification baselines;
- interpret MAE, RMSE, R², precision, recall, F1, and ROC-AUC;
- choose a decision threshold on validation data and report its trade-off.

## Prediction starts with a decision

A model score is useful only when it changes an action. Before choosing an algorithm, write down:

1. **Unit:** what one row represents.
2. **Prediction time:** when the score will be produced.
3. **Available features:** facts known at that time.
4. **Label:** the future or observed outcome to learn.
5. **Action:** what happens after the prediction.
6. **Cost:** which false positives, false negatives, delays, and abstentions matter.

For example, “predict churn” is incomplete. “Every Monday, rank active accounts using data available
through Sunday so a ten-person retention team can contact 100 accounts” defines timing, capacity, and
the decision. It also suggests precision among the top 100 may matter more than raw accuracy.

## Establish a baseline first

A **baseline** is the simplest reasonable comparison: the mean, median, majority class, recent value,
or a clear rule. It answers whether the model has earned its complexity.

```python
mean_prediction = np.repeat(y_train.mean(), repeats=len(y_validation))
baseline_mae = mean_absolute_error(y_validation, mean_prediction)
```

Compare every candidate on the same rows and metric. A sophisticated model beating a deliberately bad
baseline is weak evidence; choose a baseline that could plausibly ship.

## Split roles before fitting

The three data roles answer different questions:

| Split | Used for | Must not be used for |
|---|---|---|
| Training | fit model parameters and preprocessing | final performance claim |
| Validation or cross-validation | choose features, model, hyperparameters, and threshold | repeated public reporting as “test” |
| Test | one final estimate after choices are fixed | tuning or early stopping |

A random split assumes rows are exchangeable. That assumption fails when deployment predicts future
periods, new users, new sites, or groups with repeated records. Use a temporal split for future data
and a grouped split when records from one entity must stay together. Remove exact and near duplicates
before they can cross a boundary.

## Leakage is information from the wrong time or role

**Data leakage** happens when training uses information unavailable at prediction time or information
from validation/test rows. It can produce excellent offline metrics and poor deployed behavior.

Common forms include:

- a feature recorded after the label outcome;
- fitting imputation, scaling, vocabulary, or feature selection on all rows;
- duplicate patients or customers appearing in both train and test;
- target-derived aggregates that include the row being predicted;
- selecting a threshold after inspecting final test results.

Put learned transformations inside a scikit-learn `Pipeline`. Cross-validation then fits each step on
its training fold only:

```python
model = Pipeline(
    [
        ("scale", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=1_000)),
    ]
)
model.fit(x_train, y_train)
```

A pipeline prevents a class of implementation leaks. It cannot repair a feature whose timestamp is
after prediction time; that requires domain and data-lineage checks.

## Regression metrics answer different questions

Let the residual be `actual - prediction`.

- **MAE** averages absolute residuals. It stays in target units and treats errors linearly.
- **RMSE** takes the square root of mean squared error. Large misses receive more weight.
- **R²** compares squared error with predicting the target mean. It can be negative on evaluation
  data and does not express error in target units.

Report at least one target-unit metric. A MAE of `8.2` can be discussed as eight units; an R² of `0.7`
cannot tell a product owner the typical error size. Inspect residuals by target range, time, and
important slices because a single mean can hide systematic misses.

## Classification begins with a confusion matrix

For a chosen positive class and threshold:

| | Predicted negative | Predicted positive |
|---|---:|---:|
| Actual negative | true negative | false positive |
| Actual positive | false negative | true positive |

- **Accuracy** is the correct fraction; it can hide failures on rare positives.
- **Precision** asks: of predicted positives, how many were positive?
- **Recall** asks: of actual positives, how many were found?
- **F1** is the harmonic mean of precision and recall; it assumes one balance between them.
- **ROC-AUC** measures ranking across thresholds; it does not describe one operating decision.
- **Log loss** and **Brier score** evaluate probability quality, not only labels.

Always state which label is positive. Define what happens when there are no positive predictions, and
keep the confusion-matrix label order fixed so consumers do not swap cells.

## Scores become actions through a threshold

Many classifiers return a score or estimated probability. The default threshold `0.5` is not a law.
Lowering it usually predicts more positives, increasing recall and operational volume while often
reducing precision. Raising it usually does the reverse.

Choose the threshold on validation data using an explicit decision rule, such as:

```text
maximize precision subject to recall >= 0.80
```

Then freeze the threshold and evaluate once on test data. Also report predicted-positive count or
rate: a threshold that exceeds team capacity is not deployable even when its metric looks good.

[`threshold_tradeoff_example.py`](threshold_tradeoff_example.py) applies three thresholds to the same
fixed validation scores and prints precision, recall, and review volume.

```bash
uv run python chapters/06_ml_workflows_and_metrics/threshold_tradeoff_example.py
```

The example does not train or claim a model-quality level. It isolates the decision rule so the
trade-off is easy to see.

## Validation is an estimate, not a guarantee

Metrics vary with the sample and split. Compare slices, show counts next to rates, and use repeated
splits, cross-validation, or confidence intervals when uncertainty matters. A tiny subgroup with 100%
accuracy is not strong evidence if it contains two rows.

After aggregate evaluation, inspect representative false positives and false negatives. Look for
broken labels, leakage, unsupported populations, and product constraints before tuning the algorithm.
Offline evaluation still cannot prove causal impact; an online experiment may be needed to estimate
the effect of acting on predictions.

## Workflow pitfalls

- Reusing the test set during iteration turns it into validation data.
- Optimizing many metrics and reporting only the best one hides selection.
- Comparing models on different rows confounds model and sample changes.
- Rounding metrics before calculation or storage loses information.
- Using accuracy on rare positives can reward predicting the majority every time.
- Calling scores “probabilities” without checking calibration can mislead decision makers.
- Treating protected or operational slices as an afterthought can hide concentrated harm.

## ML evaluation checklist

- [ ] Row unit, prediction time, label window, action, and costs are written down.
- [ ] A realistic baseline is evaluated on the same rows and metric.
- [ ] The split matches time/group/duplicate behavior expected in deployment.
- [ ] Learned preprocessing is inside a pipeline and fit on training data only.
- [ ] Threshold and hyperparameters are chosen without final test information.
- [ ] Metric definitions, positive label, threshold, counts, and uncertainty are reported.
- [ ] Important slices and concrete errors are inspected.
- [ ] Reproducibility includes data version, code version, seed, and configuration.

See the full [metrics field guide](../../docs/metrics.md) for formulas and interpretation questions.

## Run it

```bash
uv run python chapters/06_ml_workflows_and_metrics/example.py
uv run python chapters/06_ml_workflows_and_metrics/threshold_tradeoff_example.py
```

The packaged scikit-learn datasets require no download. Their provenance and terms are recorded in
the [dataset manifest](../../datasets/manifest.json).

## Try it

- Change the threshold example's recall floor and explain the operational effect.
- Replace Ridge with a mean baseline and compare MAE on exactly the same rows.
- List three ways patient or customer records could leak across a random split.
- Solve [Evaluate a classifier](../../exercises/medium/04_classification_metrics/README.md).
- Solve [Select a decision threshold](../../exercises/medium/10_threshold_selection/README.md).
- Later solve the [leakage-safe pipeline](../../exercises/hard/05_risk_pipeline/README.md).

## References

- [scikit-learn model selection](https://scikit-learn.org/stable/model_selection.html) — official,
  free guide to splitting, cross-validation, and hyperparameter search.
- [Pipelines and composite estimators](https://scikit-learn.org/stable/modules/compose.html#pipeline) —
  official, free reference for fitting preprocessing with a model.
- [Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html) — official, free
  metric definitions, scoring conventions, and examples.
- [Common pitfalls and data leakage](https://scikit-learn.org/stable/common_pitfalls.html) — official,
  free examples of inconsistent preprocessing and leakage.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — free
  engineering guidance; useful for framing baselines and pipelines, not a universal private standard.
