# 05 · NumPy and pandas 📊

**Time:** 70 minutes · **Prerequisites:** [Data structures](../02_data_structures_and_iteration/README.md)

## Outcomes

You will be able to:

- reason about array shape, dtype, axis, and broadcasting;
- select, aggregate, and vectorize NumPy operations;
- load, filter, join, group, and reshape pandas data;
- treat missing values and indexes as design choices;
- move between arrays and DataFrames without losing meaning.

## NumPy: shape before values

An array has a `shape`, a `dtype`, and ordered axes. Print those before debugging individual values.
Broadcasting compares dimensions from the right and allows equal sizes or size 1.

```python
features = np.array([[1.0, 10.0], [2.0, 20.0]])  # shape (2, 2)
means = features.mean(axis=0)  # shape (2,)
centered = features - means  # broadcasts over rows
```

Vectorization moves loops into optimized array code. It is often faster and clearer, but temporary
arrays can consume memory. Measure on realistic data before making an optimization claim.

## pandas: declare row and column meaning

A DataFrame is a labeled table. Prefer explicit column selection, `.loc` for label selection, and
`.assign` for readable transformations. `groupby(...).agg(...)` follows split → apply → combine.

Common traps:

- fitting missing-value logic on all data before a train/test split;
- accidental many-to-many joins that multiply rows;
- chained assignment instead of a clear `.loc` or `.assign`;
- treating an index as a normal feature without deciding why;
- converting to `object` dtype, which can hide mixed data.

## Run it

```bash
uv run python chapters/05_numpy_and_pandas/example.py
```

The Wine dataset is packaged by scikit-learn and needs no download.

## Try it

- Group the frame by `class_name` and compare median alcohol.
- Join a small label table and assert that the row count did not change.
- Introduce one missing value and choose whether to drop or impute it.
- Solve [Build customer features](../../exercises/medium/03_customer_features/README.md).

## References

- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [pandas getting started](https://pandas.pydata.org/docs/getting_started/index.html)
- [pandas groupby guide](https://pandas.pydata.org/docs/user_guide/groupby.html)
