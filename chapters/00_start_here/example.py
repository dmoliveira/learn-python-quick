"""The first runnable course example."""

from learn_python_quick import __version__
from learn_python_quick.foundations import SaleRow, summarize_sales


def main() -> None:
    rows: list[SaleRow] = [
        {"product": "coffee", "units": 2, "unit_price": 4.5},
        {"product": "tea", "units": 3, "unit_price": 3.25},
    ]
    summary = summarize_sales(rows)
    print(f"Learn Python Quick {__version__}")
    print(f"revenue: ${summary.revenue:.2f}")
    print(f"best seller: {summary.best_seller}")


if __name__ == "__main__":
    main()
