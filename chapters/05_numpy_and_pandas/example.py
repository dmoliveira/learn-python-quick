"""Array broadcasting and labeled table aggregation."""

import numpy as np

from learn_python_quick.data import load_wine_frame


def main() -> None:
    matrix = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    centered = matrix - matrix.mean(axis=0)
    print(f"shape={centered.shape} column means={centered.mean(axis=0).round(8)}")

    wine = load_wine_frame()
    summary = (
        wine.groupby("class_name", as_index=False)
        .agg(rows=("target", "size"), mean_alcohol=("alcohol", "mean"))
        .sort_values("class_name")
    )
    print(summary.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
