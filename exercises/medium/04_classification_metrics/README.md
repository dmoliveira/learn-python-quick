# 04 · Evaluate a classifier 🩺

**Level:** 🟡 Medium · **Time:** 40–55 min · **Read first:**
[ML workflows and metrics](../../../chapters/06_ml_workflows_and_metrics/README.md)

## Problem

A risk model predicts binary labels where `1` is the positive class. Implement
`evaluate_binary_classifier(y_true, y_pred)` in [`answer.py`](answer.py).

Return:

```python
{
    "accuracy": 0.8,
    "precision": 0.75,
    "recall": 0.6,
    "f1": 0.6667,
    "confusion_matrix": [[tn, fp], [fn, tp]],
}
```

Do not round the returned floats; formatting belongs to the presentation layer.

### Contract

- Accept equal-length non-empty sequences containing labels `0` or `1` only.
- Raise `ValueError` for empty, unequal, or invalid-label input.
- Return zero precision and F1 when no positive prediction exists.
- Always return a 2×2 confusion matrix in label order `[0, 1]`.

## Hints

1. Draw the four confusion-matrix cells before writing code.
2. You may calculate manually or use `sklearn.metrics`; understand each result either way.
3. In scikit-learn, set `zero_division=0` and pass `labels=[0, 1]` to the matrix.
4. Ask whether false negatives or false positives cost more in the imagined product.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=medium/04_classification_metrics
```

Before opening the answer, explain why accuracy alone can fail on a rare-positive problem.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#04--evaluate-a-classifier), then inspect
[`classification_metrics.py`](../../../solutions/medium/classification_metrics.py).

</details>
