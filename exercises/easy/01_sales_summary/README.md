# 01 · Summarize café sales ☕

**Level:** 🟢 Easy · **Time:** 20–30 min · **Read first:** Chapters
[01](../../../chapters/01_python_fundamentals/README.md) and
[02](../../../chapters/02_data_structures_and_iteration/README.md)

## Problem

A café exports sales rows as dictionaries. Implement `summarize_sales(rows)` in
[`answer.py`](answer.py). Return:

```python
{
    "revenue": 23.25,
    "units_by_product": {"coffee": 3, "tea": 3},
    "best_seller": "coffee",
}
```

### Contract

- Each row has `product: str`, `units: int`, and `unit_price: float`.
- Strip product whitespace. Reject a blank product or negative numeric value with `ValueError`.
- Round total revenue to two decimals.
- Sort `units_by_product` by product name.
- Pick the most units; break a tie alphabetically.
- Empty input returns zero revenue, an empty dictionary, and `None` for `best_seller`.

Use [`datasets/generated/sales.csv`](../../../datasets/generated/sales.csv) as realistic input.

## Hints

1. Keep one dictionary of units per product and one collection of revenue parts.
2. `collections.defaultdict(int)` can remove an existence check.
3. A sort key like `(-units, product)` handles descending units and ascending names.
4. `math.fsum` is more stable than repeatedly adding many floats.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=easy/01_sales_summary
```

Before opening the answer, explain the tie rule and the invalid-input behavior.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#01--summarize-café-sales), then inspect
[`sales_summary.py`](../../../solutions/easy/sales_summary.py).

</details>
