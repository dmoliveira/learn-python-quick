# 07 · Plan job batches 📦

**Level:** 🟢 Easy · **Time:** 25–35 min · **Read first:** Chapters
[01](../../../chapters/01_python_fundamentals/README.md) and
[02](../../../chapters/02_data_structures_and_iteration/README.md)

## Problem

A worker receives jobs in a specific order. Implement `plan_job_batches(jobs, *, batch_size)` in
[`answer.py`](answer.py). Normalize each job, split it into fixed-size batches, and count statuses.

```python
jobs = [
    {"id": " job-1 ", "status": " QUEUED "},
    {"id": "job-2", "status": "running"},
]
```

Expected result for `batch_size=1`:

```python
{
    "batches": [
        [{"id": "job-1", "status": "queued"}],
        [{"id": "job-2", "status": "running"}],
    ],
    "status_counts": {"queued": 1, "running": 1, "succeeded": 0, "failed": 0},
}
```

### Contract

- Every job has exactly `id` and `status` string fields.
- Trim IDs; trim and lowercase statuses.
- Accept only `queued`, `running`, `succeeded`, and `failed`.
- Reject blank or duplicate normalized IDs, unknown statuses, missing/extra fields, and
  `batch_size < 1` with `ValueError`.
- Preserve input order and do not mutate the input.
- The final batch may be smaller. Empty jobs return no batches and four zero counts.

## Hints

1. Validate and normalize into a new list before creating batches.
2. Use a set for duplicate-ID detection and a dictionary or `Counter` for status counts.
3. A range stepping by `batch_size` can slice the normalized list.
4. Initialize every allowed status to zero so the output schema is stable.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. Run `make check` for
> the green repository-health check.

```bash
make exercise ID=easy/07_job_batches
```

Before revealing the answer, explain why normalization happens before duplicate checking.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach. Read the [solution reasoning](../../../solutions/README.md#07--plan-job-batches),
then inspect [`job_batches.py`](../../../solutions/easy/job_batches.py).

</details>
