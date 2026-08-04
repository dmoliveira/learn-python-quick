"""Keep order calculation pure and presentation separate."""

from __future__ import annotations

from decimal import Decimal
from typing import TypedDict


class LineItem(TypedDict):
    sku: str
    quantity: int
    unit_price: Decimal


def calculate_quote(
    items: list[LineItem],
    /,
    *,
    discount_threshold: Decimal = Decimal("50.00"),
    discount_rate: Decimal = Decimal("0.10"),
) -> dict[str, Decimal]:
    """Calculate money values without printing or mutating input."""
    if not Decimal("0") <= discount_rate <= Decimal("1"):
        raise ValueError("discount_rate must be between 0 and 1")

    subtotal = Decimal("0")
    for item in items:
        if not item["sku"].strip():
            raise ValueError("sku must not be blank")
        if item["quantity"] < 0 or item["unit_price"] < 0:
            raise ValueError("quantity and unit_price must be non-negative")
        subtotal += item["quantity"] * item["unit_price"]

    discount = subtotal * discount_rate if subtotal >= discount_threshold else Decimal("0")
    return {"subtotal": subtotal, "discount": discount, "total": subtotal - discount}


def format_quote(quote: dict[str, Decimal]) -> str:
    """Presentation can change without changing business rules."""
    return (
        f"subtotal=${quote['subtotal']:.2f} "
        f"discount=${quote['discount']:.2f} total=${quote['total']:.2f}"
    )


def main() -> None:
    items: list[LineItem] = [
        {"sku": "book", "quantity": 2, "unit_price": Decimal("24.00")},
        {"sku": "course", "quantity": 1, "unit_price": Decimal("20.00")},
    ]
    before = [item.copy() for item in items]
    quote = calculate_quote(items, discount_rate=Decimal("0.10"))
    assert items == before
    print(format_quote(quote))


if __name__ == "__main__":
    main()
