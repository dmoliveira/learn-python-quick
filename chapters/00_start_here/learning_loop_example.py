"""Practice predict, run, change, test, and explain on one tiny problem."""

from learn_python_quick.foundations import SaleRow, summarize_sales


def main() -> None:
    rows: list[SaleRow] = [
        {"product": "tea", "units": 2, "unit_price": 3.25},
        {"product": "coffee", "units": 1, "unit_price": 4.5},
    ]

    predicted_revenue = 11.0
    print(f"prediction: revenue should be ${predicted_revenue:.2f}")
    summary = summarize_sales(rows)
    assert summary.revenue == predicted_revenue
    print(f"evidence: revenue is ${summary.revenue:.2f}")

    try:
        summarize_sales([{"product": "tea", "units": -1, "unit_price": 3.25}])
    except ValueError as error:
        print(f"expected boundary failure: {error}")

    print("next: change one quantity, predict again, then run make check")


if __name__ == "__main__":
    main()
