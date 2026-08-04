"""Solution: summarize pandas missingness with explicit empty-table behavior."""

from __future__ import annotations

import pandas as pd


def summarize_missing_values(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.columns.empty:
        raise ValueError("columns must not be empty")
    if frame.columns.has_duplicates:
        raise ValueError("columns must be unique")
    if not all(isinstance(column, str) for column in frame.columns):
        raise ValueError("columns must use string names")

    summary = frame.isna().sum().rename_axis("column").reset_index(name="missing_count")
    if frame.empty:
        summary["missing_rate"] = 0.0
    else:
        summary["missing_rate"] = summary["missing_count"] / len(frame)

    return summary.sort_values(
        ["missing_count", "column"],
        ascending=[False, True],
    ).reset_index(drop=True)
