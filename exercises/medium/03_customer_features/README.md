# 03 · Build customer features 🧾

**Level:** 🟡 Medium · **Time:** 45–60 min · **Read first:**
[NumPy and pandas](../../../chapters/05_numpy_and_pandas/README.md)

## Problem

Turn raw customer events into one feature row per customer. Implement `build_customer_features` in
[`answer.py`](answer.py).

Input columns:

```text
customer_id | event (purchase/support/visit) | amount | occurred_at
```

Output columns, in this order:

```text
customer_id | purchase_count | total_spend | support_tickets | last_event_at
```

### Contract

- Return one row per customer, sorted by `customer_id`, with a fresh 0-based index.
- Count purchase and support events separately.
- Sum `amount` only for purchases; customers without purchases receive `0.0`.
- Parse `last_event_at` as a timezone-aware UTC datetime.
- Do not mutate the input frame.
- Raise `ValueError` containing `missing` when a required column is absent.

Explore [`customer_events.csv`](../../../datasets/generated/customer_events.csv) first.

## Hints

1. Validate `required_columns - set(events.columns)` before transforming.
2. Work on `events.copy()` and parse time with `pd.to_datetime(..., utc=True)`.
3. Create numeric indicator columns, then use one `groupby().agg(...)`.
4. Test one customer with no purchases.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=medium/03_customer_features
```

Before opening the answer, explain why the input is copied and why output row order is part of the
contract.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#03--build-customer-features), then inspect
[`customer_features.py`](../../../solutions/medium/customer_features.py).

</details>
