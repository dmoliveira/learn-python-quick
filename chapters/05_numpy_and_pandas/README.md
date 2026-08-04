# 05 · NumPy and pandas 📊

**Time:** 70 minutes · **Prerequisites:** [Data structures](../02_data_structures_and_iteration/README.md)

## Outcomes

You will be able to:

- reason about array shape, dtype, axis, and broadcasting;
- select, aggregate, and vectorize NumPy operations;
- state what one DataFrame row represents before transforming it;
- load, filter, join, group, and reshape pandas data;
- treat missing values, indexes, and joins as design choices;
- move between arrays and DataFrames without losing meaning.

## Two data models

A NumPy array is a rectangular block of values with one data type. Its meaning comes from the code
around it: shape `(200, 4)` does not say whether rows are customers, images, or time steps. A pandas
DataFrame adds row and column labels and allows different column types.

Use NumPy for dense numerical operations. Use pandas when labels, mixed types, joins, or grouped
business records matter. Moving between them is normal, but write down what each axis means first.

```text
array:     position + shape + dtype
DataFrame: row meaning + column schema + index
```

## NumPy: shape before values

An array has a `shape`, a `dtype`, and ordered axes. Print those before debugging individual values.
For a two-dimensional feature matrix, axis 0 usually contains rows and axis 1 contains features:

```python
features = np.array([[1.0, 10.0], [2.0, 20.0]])  # shape (2, 2)
means = features.mean(axis=0)  # one mean per column, shape (2,)
centered = features - means  # subtract those means from every row
```

The axis passed to a reduction is the axis that disappears:

| Expression | Result | Meaning for a row-by-feature matrix |
|---|---|---|
| `features.sum()` | scalar | sum every value |
| `features.sum(axis=0)` | one value per column | sum down the rows |
| `features.sum(axis=1)` | one value per row | sum across the features |

### Broadcasting is shape alignment

Broadcasting lets NumPy combine compatible shapes without manually repeating data. NumPy compares
dimensions from the right. Each pair must be equal or one of them must be `1`.

```text
(3, 4) and    (4,) → compatible: apply one four-value row to all three rows
(3, 4) and  (3, 1) → compatible: apply one value to each row
(3, 4) and    (3,) → incompatible: trailing dimensions 4 and 3 disagree
```

Add dimensions deliberately with `values[:, None]` or `np.expand_dims`. Do not reshape repeatedly
until an error disappears; that can produce a valid shape with the wrong meaning.

### Vectorization, views, and copies

Vectorization moves element-wise work into array operations. It is usually clearer and faster than a
Python loop for numerical data, but several intermediate arrays can increase memory use. Measure on
realistic data before making a performance claim.

Basic slicing often returns a **view**, which shares memory with the source array. Fancy indexing and
boolean indexing usually return copies. If independent data is required, call `.copy()` explicitly.
Treat unexpected mutation as a contract bug, not merely a NumPy surprise.

## pandas: declare row and column meaning

Before a transformation, complete this sentence: “One row represents ___.” This is the table's
**grain**. A join or group operation often changes the grain, and that should be intentional.

Prefer explicit column selection, `.loc` for label-based selection, and `.assign` for readable
transformations:

```python
active = customers.loc[customers["status"] == "active", ["customer_id", "spend"]].assign(
    spend_bucket=lambda frame: frame["spend"].ge(100).map({True: "high", False: "low"})
)
```

`groupby(...).agg(...)` follows split → apply → combine. Named aggregation makes output names and
operations visible:

```python
summary = events.groupby("customer_id", as_index=False).agg(
    event_count=("event", "size"),
    total_amount=("amount", "sum"),
)
```

Avoid chained assignment such as `frame[mask]["value"] = 0`. The intermediate object may be a copy.
Use `frame.loc[mask, "value"] = 0`, or create a transformed frame with `.assign`.

## Missing values need a policy

Missing does not always mean the same thing. It may mean “not measured,” “not applicable,” “not yet
known,” or “lost in transport.” First measure missingness by column and relevant data slice. Then
choose a policy that matches that meaning.

- **Drop:** appropriate only when the lost rows/columns are acceptable and not systematically biased.
- **Constant fill:** makes “missing” explicit for categories; it can distort numeric distance.
- **Learned imputation:** fit the imputer on training data only, inside the model pipeline.
- **Missing indicator:** can preserve useful absence information, but may encode process bias.

`NaN` is not equal to itself, so use `isna()`/`notna()` instead of equality checks. Nullable integer,
boolean, and string dtypes can preserve meaning better than falling back to generic `object` values.

## Joins are cardinality decisions

A join states how rows on the left relate to rows on the right. Duplicate keys can silently multiply
records. Use pandas validation when the expected relationship is known:

```python
enriched = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
    indicator=True,
)
```

Check row counts, unmatched keys, duplicate keys, and nulls introduced by the join. An index is not
automatically a feature or a stable identifier; decide its purpose before resetting, persisting, or
feeding it to a model.

## Worked problem: profile a small table

[`dataframe_quality_example.py`](dataframe_quality_example.py) creates an in-memory event table,
reports column dtype and missingness, then enriches it with a many-to-one join. The script asserts the
join keeps the original row count, so an accidental duplicate lookup key fails close to its cause.

```bash
uv run python chapters/05_numpy_and_pandas/dataframe_quality_example.py
```

The data is generated in the script. It uses no file or network and produces the same result on every
run. For a reusable production report, define the output schema and put that behavior in a tested
package module rather than copying the example.

## Common data-table pitfalls

- Fitting missing-value logic on all data before a train/test split leaks future information.
- Accidental many-to-many joins multiply rows and change metric denominators.
- Chained assignment makes it unclear whether the original frame changed.
- Converting to `object` dtype can hide mixed values and slow calculations.
- Calling `.values` or `.to_numpy()` discards labels; preserve column order separately.
- Row-by-row `apply(axis=1)` is often slower and less explicit than column operations.
- Comparing floating-point arrays with exact equality ignores representation error; use tolerances.

## Data transformation checklist

- [ ] The row grain and each important column's meaning are written down.
- [ ] Shape, dtypes, unique keys, and missingness are inspected before transformation.
- [ ] Array axes and broadcast dimensions have explicit meaning.
- [ ] Input mutation versus copying is an intentional contract choice.
- [ ] Join cardinality is validated and unmatched keys are measured.
- [ ] Learned preprocessing is fit on training data only.
- [ ] Output row order, column order, and index behavior are deterministic when public.
- [ ] Large-data assumptions are measured rather than inferred from a tiny sample.

## Run it

```bash
uv run python chapters/05_numpy_and_pandas/example.py
uv run python chapters/05_numpy_and_pandas/dataframe_quality_example.py
```

The Wine dataset used by `example.py` is packaged by scikit-learn and needs no download. Its source,
terms, and network behavior are recorded in the [dataset manifest](../../datasets/manifest.json).

## Try it

- Group the Wine frame by `class_name` and compare median alcohol.
- Change the quality example's lookup table to contain a duplicate key and read the merge error.
- Introduce one missing value and explain whether dropping or imputing it fits its meaning.
- Solve [Build customer features](../../exercises/medium/03_customer_features/README.md).
- Solve [Summarize missing values](../../exercises/medium/09_missing_values/README.md).

## References

- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) — official, free introduction
  to arrays, axes, indexing, and vectorized calculations.
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) — official, free
  shape-compatibility rules and visual examples.
- [pandas getting started](https://pandas.pydata.org/docs/getting_started/index.html) — official, free
  tutorials for selection, grouping, reshaping, and joins.
- [pandas merge guide](https://pandas.pydata.org/docs/user_guide/merging.html) — official, free details
  on join types, cardinality validation, and indicators.
- [Python for Data Analysis, 3E](https://wesmckinney.com/book/) by Wes McKinney — author-published,
  free online book with deeper NumPy and pandas workflows; examples target the listed edition.
