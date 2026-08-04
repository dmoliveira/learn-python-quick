"""Measure readable loop and vectorized implementations without fragile claims."""

from time import perf_counter

import numpy as np

from learn_python_quick.performance import fibonacci, zscore_with_numpy, zscore_with_python


def main() -> None:
    values = np.linspace(-10, 10, 50_000)

    started = perf_counter()
    python_result = zscore_with_python(values.tolist())
    python_seconds = perf_counter() - started

    started = perf_counter()
    numpy_result = zscore_with_numpy(values)
    numpy_seconds = perf_counter() - started

    print(f"same result={np.allclose(python_result, numpy_result)}")
    print(f"loop={python_seconds:.6f}s numpy={numpy_seconds:.6f}s")
    print(f"cached pure function: fibonacci(20)={fibonacci(20)}")


if __name__ == "__main__":
    main()
