"""Typed, testable examples of modern Python foundations."""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass
from enum import StrEnum
from itertools import islice
from typing import TypedDict, TypeVar

T = TypeVar("T")


class SaleRow(TypedDict):
    """One validated sales input row."""

    product: str
    units: int
    unit_price: float


@dataclass(frozen=True, slots=True)
class SalesSummary:
    """A compact result that is immutable and cheap to inspect."""

    revenue: float
    units_by_product: dict[str, int]
    best_seller: str | None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


def summarize_sales(rows: Iterable[SaleRow]) -> SalesSummary:
    """Aggregate sales in one pass and reject invalid business values."""
    units_by_product: defaultdict[str, int] = defaultdict(int)
    revenue_parts: list[float] = []

    for row in rows:
        product = row["product"].strip()
        units = row["units"]
        unit_price = row["unit_price"]
        if not product:
            raise ValueError("product must not be blank")
        if units < 0 or unit_price < 0:
            raise ValueError("units and unit_price must be non-negative")
        units_by_product[product] += units
        revenue_parts.append(units * unit_price)

    best_seller = min(
        units_by_product,
        key=lambda product: (-units_by_product[product], product),
        default=None,
    )
    return SalesSummary(
        revenue=round(math.fsum(revenue_parts), 2),
        units_by_product=dict(sorted(units_by_product.items())),
        best_seller=best_seller,
    )


def batched(items: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Yield fixed-size tuples without loading the whole iterable into memory."""
    if size < 1:
        raise ValueError("size must be at least 1")
    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch


def safe_divide(numerator: float, denominator: float, *, default: float = 0.0) -> float:
    """Show a keyword-only fallback for an expected zero denominator."""
    return default if denominator == 0 else numerator / denominator


def format_metric(name: str, value: float, /, *, digits: int = 3) -> str:
    """Use positional-only and keyword-only arguments to make calls unambiguous."""
    if digits < 0:
        raise ValueError("digits must be non-negative")
    return f"{name}: {value:.{digits}f}"


def next_action(status: JobStatus) -> str:
    """Use structural pattern matching for a small state decision."""
    match status:
        case JobStatus.QUEUED:
            return "wait"
        case JobStatus.RUNNING:
            return "observe"
        case JobStatus.SUCCEEDED:
            return "publish"
        case JobStatus.FAILED:
            return "inspect logs"
