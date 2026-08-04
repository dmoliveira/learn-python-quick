"""Solution: normalize once, validate IDs, then batch without mutating input."""

from __future__ import annotations

STATUSES = ("queued", "running", "succeeded", "failed")


def plan_job_batches(
    jobs: list[dict[str, str]],
    *,
    batch_size: int,
) -> dict[str, object]:
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    normalized: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    counts = dict.fromkeys(STATUSES, 0)

    for job in jobs:
        if set(job) != {"id", "status"}:
            raise ValueError("every job must contain exactly id and status")
        job_id = job["id"].strip()
        status = job["status"].strip().lower()
        if not job_id:
            raise ValueError("job id must not be blank")
        if job_id in seen_ids:
            raise ValueError(f"duplicate job id: {job_id}")
        if status not in STATUSES:
            raise ValueError(f"unknown status: {status}")
        seen_ids.add(job_id)
        counts[status] += 1
        normalized.append({"id": job_id, "status": status})

    batches = [
        normalized[index : index + batch_size] for index in range(0, len(normalized), batch_size)
    ]
    return {"batches": batches, "status_counts": counts}
