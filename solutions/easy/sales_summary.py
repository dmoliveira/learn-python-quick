"""Solution: aggregate sales in one pass with deterministic tie-breaking."""

from __future__ import annotations

import math
from collections import defaultdict


def summarize_sales(rows: list[dict[str, object]]) -> dict[str, object]:
    units_by_product: defaultdict[str, int] = defaultdict(int)
    revenue_parts: list[float] = []

    for row in rows:
        product_value = row.get("product")
        units_value = row.get("units")
        price_value = row.get("unit_price")
        if not isinstance(product_value, str) or not product_value.strip():
            raise ValueError("product must be a non-blank string")
        if not isinstance(units_value, int) or isinstance(units_value, bool):
            raise ValueError("units must be an integer")
        if not isinstance(price_value, int | float) or isinstance(price_value, bool):
            raise ValueError("unit_price must be numeric")
        if units_value < 0 or price_value < 0:
            raise ValueError("units and unit_price must be non-negative")

        product = product_value.strip()
        units_by_product[product] += units_value
        revenue_parts.append(units_value * float(price_value))

    ordered_units = dict(sorted(units_by_product.items()))
    best_seller = min(
        ordered_units,
        key=lambda product: (-ordered_units[product], product),
        default=None,
    )
    return {
        "revenue": round(math.fsum(revenue_parts), 2),
        "units_by_product": ordered_units,
        "best_seller": best_seller,
    }
