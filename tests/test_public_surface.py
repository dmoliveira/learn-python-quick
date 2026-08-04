from __future__ import annotations

import numpy as np
import pytest

from learn_python_quick.cli import main
from learn_python_quick.performance import fibonacci, zscore_with_numpy, zscore_with_python


def test_roadmap_starts_with_orientation_and_links_progress(
    capsys: pytest.CaptureFixture[str],
) -> None:
    main(["roadmap"])
    output = capsys.readouterr().out
    assert "Start: Chapter 00" in output
    assert "docs/learning-paths.md#my-progress" in output


def test_zscore_implementations_match_and_handle_constant_values() -> None:
    values = [1.0, 2.0, 3.0, 4.0]
    assert zscore_with_python(values) == pytest.approx(zscore_with_numpy(values))
    assert zscore_with_python([2.0, 2.0]) == [0.0, 0.0]
    assert np.array_equal(zscore_with_numpy([2.0, 2.0]), np.zeros(2))
    assert zscore_with_python([]) == []


def test_fibonacci_validates_and_uses_its_cache() -> None:
    fibonacci.cache_clear()
    assert fibonacci(20) == 6765
    first = fibonacci.cache_info()
    assert fibonacci(20) == 6765
    assert fibonacci.cache_info().hits > first.hits
    with pytest.raises(ValueError, match="non-negative"):
        fibonacci(-1)
