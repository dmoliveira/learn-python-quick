# 09 · Summarize missing values 🧭

**Level:** 🟡 Medium · **Time:** 40–55 min · **Read first:**
[NumPy and pandas](../../../chapters/05_numpy_and_pandas/README.md)

## Problem

A data-quality check needs one deterministic row per input column. Implement
`summarize_missing_values(frame)` in [`answer.py`](answer.py).

For this input:

```python
pd.DataFrame(
    {
        "country": ["BR", None, "US", None],
        "age": [31.0, 44.0, None, 27.0],
        "plan": ["pro", "free", "pro", "free"],
    }
)
```

return:

```text
  column  missing_count  missing_rate
 country              2          0.50
     age              1          0.25
    plan              0          0.00
```

The output helps an engineer see the largest gaps first without inspecting private row values.

### Contract

- Accept a pandas DataFrame whose column names are unique strings.
- Return a new DataFrame with columns in this exact order:
  `column`, `missing_count`, `missing_rate`.
- Return one row per input column. Count every value recognized by pandas `isna()`.
- Calculate `missing_rate` as `missing_count / input_row_count` without rounding.
- Sort by `missing_count` descending, then `column` ascending; return a fresh 0-based index.
- For a frame with columns but zero rows, return zero count and `0.0` rate for every column.
- Raise `ValueError` containing `columns` when the frame has no columns, duplicate column names, or a
  non-string column name.
- Do not mutate the input frame or its index.

## Why the edge cases matter

Dividing by zero can create `NaN`, which is a poor result for an otherwise valid empty table schema.
Stable tie ordering makes reports and tests reproducible. Unique string names keep the output's
`column` field and alphabetical tie rule unambiguous.

## Hints

1. Validate `frame.columns` before calculating.
2. `frame.isna().sum()` returns one count per column.
3. Handle `len(frame) == 0` before dividing.
4. `rename_axis(...).reset_index(...)` can turn a labeled Series into a DataFrame.
5. Pass two columns and two ascending flags to `sort_values`, then call `reset_index(drop=True)`.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=medium/09_missing_values
```

Before opening the answer, test a zero-row frame with two columns. Explain why returning zero rates is
more useful than returning missing or infinite rates.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#09--summarize-missing-values), then inspect
[`missing_values.py`](../../../solutions/medium/missing_values.py).

</details>
