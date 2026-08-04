# 07 · Trees and XGBoost 🌲

**Time:** 60 minutes · **Prerequisites:** [ML workflows](../06_ml_workflows_and_metrics/README.md)

## Outcomes

You will be able to:

- explain how decision trees partition feature space;
- control depth and minimum samples to reduce overfitting;
- compare bagging/random forests with gradient boosting;
- train a small XGBoost classifier with early stopping;
- keep validation and test roles separate during boosting;
- inspect importance carefully without turning it into causality.

## A tree is a sequence of questions

A decision tree repeatedly asks a threshold question such as `age <= 37.5`. Each split partitions the
rows, and each leaf returns a prediction from the training rows that reached it. Trees can model
nonlinear effects and feature interactions without scaling numeric columns first.

```text
monthly_spend <= 62?
├── yes: support_tickets <= 1? → low/high risk leaf
└── no:  plan == "pro"?        → low/high risk leaf
```

Training selects splits that reduce an impurity measure for classification or error for regression.
The chosen split describes an association in the training data, not a causal rule.

## Capacity controls memorization

An unconstrained tree can keep splitting until leaves contain very few rows. Training performance may
be perfect while validation performance falls. Compare both, and start with a deliberately shallow
tree.

| Control | Smaller or stricter value usually does what? |
|---|---|
| `max_depth` | limits the number of sequential interactions |
| `min_samples_leaf` | requires more evidence in each leaf |
| `min_samples_split` | prevents splitting very small nodes |
| `max_features` | limits features considered at a split |
| pruning parameter | removes splits whose gain does not justify complexity |

These controls trade variance for bias. Do not tune them on the final test set. Use cross-validation
or a validation set that matches deployment.

## Ensembles combine different trees

An **ensemble** combines several models.

| Method | How trees are built | Main intuition |
|---|---|---|
| Decision tree | one tree | interpretable local rules, high variance |
| Bagging | independent trees on resampled rows | average unstable models |
| Random forest | bagging plus random feature subsets | decorrelate trees before averaging |
| Gradient boosting | each tree follows the current errors | improve one additive model in stages |

Random forests are a strong low-tuning baseline for tabular data. They can train trees in parallel and
average predictions. Gradient boosting is sequential: each new tree is chosen to improve the current
ensemble's objective, so learning rate and number of rounds interact.

## Gradient boosting is staged correction

Start with a simple prediction, measure its errors according to a loss function, then add a small tree
that improves those errors. Repeat:

```text
prediction = initial_guess
for each round:
    correction = small_tree(current_loss_gradient)
    prediction += learning_rate * correction
```

This is intuition rather than the complete algorithm. Modern libraries add regularization,
subsampling, missing-value routing, efficient histograms, and objective-specific mathematics.

Important XGBoost controls:

| Parameter | Effect |
|---|---|
| `max_depth` | interaction complexity per tree |
| `learning_rate` | contribution of each boosted tree |
| `n_estimators` | maximum boosting rounds |
| `min_child_weight` | minimum evidence required in a child |
| `subsample` / `colsample_bytree` | row/feature sampling and regularization |
| `reg_alpha` / `reg_lambda` | L1/L2 regularization on leaf weights |
| early stopping | stop after validation no longer improves |

A smaller learning rate often needs more rounds. Changing both at once makes the source of a result
harder to understand.

## Early stopping needs three roles

Early stopping observes a validation metric during training and keeps the best boosting round. Since
that process selects model complexity, the validation data is part of tuning.

```text
outer train ── split ──> fit rows + early-stopping validation rows
outer test  ───────────> one evaluation after the best round is fixed
```

Never use the final test set in `eval_set`. The course XGBoost helper first creates an outer
train/test split, then splits the outer training rows again. For a stronger estimate, repeat the
process or use nested/cross-validated tuning while keeping time and group boundaries intact.

## Worked comparison

The core example compares a depth-limited decision tree and a small random forest on exactly the same
offline split:

```bash
uv run python chapters/07_trees_and_xgboost/example.py
```

The script reports test accuracy as a compact demonstration, not proof that one algorithm is always
better. A real comparison should include a baseline, cross-validation variation, class-sensitive
metrics, runtime, and error slices.

The optional example trains bounded XGBoost rounds with one CPU worker:

```bash
uv sync --dev --extra boost
uv run python chapters/07_trees_and_xgboost/xgboost_example.py
```

XGBoost is an optional dependency, so importing the core package does not import it. This keeps the
default installation smaller and lets learners complete the core path without a compiled extension.
The course supports the version range in `pyproject.toml`; consult that installed version's docs when
an older web example puts early-stopping arguments in a different API location.

Both examples use the packaged Breast Cancer Wisconsin dataset with no network access. Review its
source and terms in the [dataset manifest](../../datasets/manifest.json). The names reflect the source
dataset; predictions are educational only and must not be used for diagnosis.

## Importance explains model use, not cause

Built-in tree importance often totals how much a feature reduced the training objective. It can favor
high-cardinality or frequently available features. Correlated features may divide, duplicate, or hide
one another's importance.

Permutation importance measures the metric change after shuffling a feature on held-out data. It is
still associational and can be misleading when shuffling creates unrealistic combinations. SHAP and
local path explanations also describe a fitted model, not what would happen under an intervention.

Use several views:

1. held-out permutation importance;
2. error and metric slices;
3. stability across folds or seeds;
4. domain review of suspicious proxies and timestamps;
5. direct tests of decision policies when causal impact matters.

## Tree-model pitfalls

- Comparing training scores only rewards memorization.
- Tuning early stopping on test data makes the test estimate optimistic.
- Encoding categories as arbitrary integers gives splits an invented order.
- Reading importance as causality turns model association into an unsupported claim.
- Increasing tree count without bounding CPU, memory, and latency can make an experiment unshippable.
- Leaving seeds, thread counts, and library versions implicit makes runs harder to reproduce.
- Assuming missing-value support makes missingness unbiased ignores how the data was collected.

## Tree experiment checklist

- [ ] A simple rule, linear model, or shallow tree provides a baseline.
- [ ] Train, validation, and test roles match the decision workflow.
- [ ] Depth, leaf size, rounds, learning rate, and early stopping are recorded.
- [ ] The same rows and metrics are used for model comparison.
- [ ] CPU threads, runtime, memory, seed, and library version are recorded.
- [ ] Important slices and representative errors are inspected.
- [ ] Importance is described as model behavior, not causal evidence.
- [ ] The optional dependency remains outside the core import path.

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

- Compare tree depths 2, 4, and unlimited on both train and validation accuracy.
- Change one XGBoost regularization parameter at a time and keep the split fixed.
- Report runtime and metric variation; do not call one split's difference a general improvement.
- Permute one held-out feature and explain what the metric change does and does not mean.
- Try [Tune boosted trees](../../docs/exercise-guide.md#challenge-catalog).

## References

- [scikit-learn decision trees](https://scikit-learn.org/stable/modules/tree.html) — official, free
  guide to tree construction, controls, strengths, and limitations.
- [scikit-learn ensemble methods](https://scikit-learn.org/stable/modules/ensemble.html) — official,
  free comparison of forests and gradient-boosted methods.
- [XGBoost Python API](https://xgboost.readthedocs.io/en/stable/python/python_api.html) — official,
  free API for the currently documented stable release; check the installed version.
- [XGBoost parameter guide](https://xgboost.readthedocs.io/en/stable/parameter.html) — official, free
  definitions for tree, learning, regularization, and task parameters.
- [Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/) by Christoph
  Molnar — author-published, free online book on permutation importance, local explanations, and their
  limits.
