# 11 · Prepare tensor batches 🧱

**Level:** 🔴 Hard · **Time:** 75–100 min · **Read first:**
[NumPy and pandas](../../../chapters/05_numpy_and_pandas/README.md) and
[PyTorch and image models](../../../chapters/08_pytorch_and_images/README.md)

## Problem

A training loop needs reproducible mini-batches while the core exercise remains usable without
installing PyTorch. Implement
`prepare_training_batches(features, labels, batch_size, seed=42)` in [`answer.py`](answer.py).

Return a list of `(feature_batch, label_batch)` NumPy array pairs. The resulting dtypes can be passed
directly to `torch.tensor` after the optional PyTorch extra is installed.

For five rows and `batch_size=2`, return three batch pairs with row counts `2`, `2`, and `1`.
Features and labels must be shuffled by the same permutation so each label stays with its row.

### Contract

- Accept a non-empty-column 2D feature array and a 1D label array with the same row count.
- Features must contain finite real numeric values. Return feature batches with dtype `float32`.
- Labels must use a non-boolean integer dtype and contain non-negative values. Return label batches
  with dtype `int64`.
- `batch_size` must be a positive non-boolean integer.
- `seed` must be a non-negative non-boolean integer.
- Generate row order with `np.random.default_rng(seed).permutation(row_count)`.
- Apply that one order to features and labels, then make consecutive batches. Keep the final short
  batch instead of dropping it.
- When features have shape `(0, feature_count)` and labels are empty, return `[]`.
- Raise `ValueError` for a broken input rule, including zero feature columns.
- Return fresh arrays that do not share memory with either input. Do not mutate either input.

## Why this is core-only

Shuffling, shape validation, and batching are data-boundary concerns. NumPy is enough to test them.
The training loop may later convert each pair:

```python
feature_tensor = torch.tensor(feature_batch, dtype=torch.float32)
label_tensor = torch.tensor(label_batch, dtype=torch.long)
```

Keeping PyTorch out of the public contract makes the exercise fast and lets failures point to the
batch logic rather than an optional installation.

## Hints

1. Inspect the original arrays' dimensions and dtypes before converting them.
2. Treat boolean arrays separately because NumPy does not consider them valid training labels here.
3. Validate finite values with `np.isfinite` after converting valid real features to `float32`.
4. Create one permutation and index both arrays with it.
5. Slice `range(0, row_count, batch_size)` and call `.copy()` on each returned slice.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=hard/11_tensor_batches
```

Before opening the answer, concatenate all output batches and prove that the same seed produces the
same aligned order without changing the input arrays.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#11--prepare-tensor-batches), then inspect
[`tensor_batches.py`](../../../solutions/hard/tensor_batches.py).

</details>
