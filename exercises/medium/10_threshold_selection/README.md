# 10 · Select a decision threshold 🎚️

**Level:** 🟡 Medium · **Time:** 50–70 min · **Read first:**
[ML workflows and metrics](../../../chapters/06_ml_workflows_and_metrics/README.md)

## Problem

A review team needs enough recall without sending every item to manual review. Implement
`select_decision_threshold(y_true, probabilities, minimum_recall)` in [`answer.py`](answer.py).

For each distinct observed probability, predict positive when `probability >= threshold`. Keep
candidates whose recall is at least `minimum_recall`. Select the candidate with highest precision;
if precision ties, select the higher threshold.

Example:

```python
select_decision_threshold(
    [1, 0, 1, 0, 1],
    [0.9, 0.8, 0.7, 0.6, 0.4],
    minimum_recall=2 / 3,
)
```

returns:

```python
{
    "threshold": 0.7,
    "precision": 2 / 3,
    "recall": 2 / 3,
    "predicted_positive": 3,
}
```

Do not round returned values. Formatting belongs to the caller.

### Contract

- Accept equal-length, non-empty sequences.
- Labels must be integer `0` or `1`; booleans are invalid labels.
- Probabilities must be finite real numbers from `0.0` through `1.0`; booleans are invalid.
- `minimum_recall` must be a finite real number in `(0.0, 1.0]`; booleans are invalid.
- Raise `ValueError` when an input rule is broken or when `y_true` has no positive label.
- Evaluate each distinct observed probability as a threshold using `score >= threshold`.
- Among candidates meeting the recall floor, maximize precision. On a precision tie, choose the
  higher threshold.
- Return exactly `threshold`, `precision`, `recall`, and `predicted_positive`.
- Return the threshold, precision, and recall as floats and the count as an integer.
- Do not mutate either input sequence.

Because the lowest observed threshold predicts every row positive, a valid input containing at least
one positive label always has a candidate with recall `1.0`.

## Hints

1. Validate and copy values into plain lists before evaluating candidates.
2. Sort `set(probabilities)` in descending order for deterministic iteration.
3. For each threshold, calculate true positives, predicted positives, and total positives.
4. Recall is `true_positives / total_positives`; precision is
   `true_positives / predicted_positives`.
5. A tuple such as `(precision, threshold)` expresses both maximization and the tie rule.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=medium/10_threshold_selection
```

Before opening the answer, create two thresholds with equal precision and verify the higher one wins.
Explain why this selection belongs on validation data rather than final test data.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#10--select-a-decision-threshold), then inspect
[`threshold_selection.py`](../../../solutions/medium/threshold_selection.py).

</details>
