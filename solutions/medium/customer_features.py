"""Solution: create typed customer aggregations without mutating input."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {"customer_id", "event", "amount", "occurred_at"}
OUTPUT_COLUMNS = [
    "customer_id",
    "purchase_count",
    "total_spend",
    "support_tickets",
    "last_event_at",
]


def build_customer_features(events: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(events.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    frame = events.copy(deep=True)
    frame["occurred_at"] = pd.to_datetime(frame["occurred_at"], utc=True, errors="raise")
    frame["amount"] = pd.to_numeric(frame["amount"], errors="raise")
    frame["is_purchase"] = (frame["event"] == "purchase").astype(int)
    frame["purchase_amount"] = frame["amount"].where(frame["event"] == "purchase", 0.0)
    frame["is_support"] = (frame["event"] == "support").astype(int)

    features = (
        frame.groupby("customer_id", as_index=False, sort=True)
        .agg(
            purchase_count=("is_purchase", "sum"),
            total_spend=("purchase_amount", "sum"),
            support_tickets=("is_support", "sum"),
            last_event_at=("occurred_at", "max"),
        )
        .reset_index(drop=True)
    )
    return features.loc[:, OUTPUT_COLUMNS]
