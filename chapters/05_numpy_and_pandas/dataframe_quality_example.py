"""Profile missing values and validate a table join without external data."""

import pandas as pd


def main() -> None:
    events = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c1", "c3"],
            "channel": ["web", "store", None, "web"],
            "duration_seconds": [42.0, 18.0, 31.0, None],
        }
    )
    missing = pd.DataFrame(
        {
            "dtype": events.dtypes.astype(str),
            "missing_count": events.isna().sum(),
            "missing_rate": events.isna().mean(),
        }
    ).rename_axis("column")
    print(missing.reset_index().to_string(index=False))

    customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c3"],
            "plan": ["pro", "free", "pro"],
        }
    )
    enriched = events.merge(customers, on="customer_id", how="left", validate="many_to_one")
    assert len(enriched) == len(events)
    print(f"rows before/after join={len(events)}/{len(enriched)}")
    print(enriched.to_string(index=False))


if __name__ == "__main__":
    main()
