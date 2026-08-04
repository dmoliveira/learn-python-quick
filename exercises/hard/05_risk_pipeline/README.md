# 05 · Train a leakage-safe risk model 🧪

**Level:** 🔴 Hard · **Time:** 90–120 min · **Read first:** Chapters
[03](../../../chapters/03_types_oop_and_pydantic/README.md),
[05](../../../chapters/05_numpy_and_pandas/README.md), and
[06](../../../chapters/06_ml_workflows_and_metrics/README.md)

## Problem

Build an **unfitted** scikit-learn `Pipeline` for mixed customer features. Implement
`build_risk_pipeline(*, seed=42)` in [`answer.py`](answer.py).

Input features:

- numeric: `age`, `monthly_spend`;
- categorical: `country`, `plan`;
- values can be missing;
- prediction can contain a country not seen during training.

### Contract

- Return a `Pipeline` with steps named exactly `preprocess` and `model`.
- Use a `ColumnTransformer` for numeric and categorical branches.
- Impute numeric values, then scale them.
- Impute categorical values, then one-hot encode with unknown categories ignored.
- Finish with logistic regression using the provided seed and enough iterations to converge.
- Do not fit anything inside the builder or mutate training input.

The public test fits on a deterministic generated dataset and checks a broad quality floor. A real
project would use a time/group-aware split, cross-validation, calibration, fairness slices, and a
separate final test.

## Design before code

Sketch this graph:

```text
numeric columns → imputer → scaler ┐
                                   ├→ combined matrix → logistic regression
categorical cols → imputer → OHE   ┘
```

Putting every learned transform inside the pipeline ensures each validation fold fits it only on
that fold's training rows.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=hard/05_risk_pipeline
```

Before opening the answer, explain where leakage would occur if imputation ran before a split.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#05--train-a-leakage-safe-risk-model), then inspect
[`risk_pipeline.py`](../../../solutions/hard/risk_pipeline.py).

</details>
