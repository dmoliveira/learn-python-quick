from __future__ import annotations

import sys

import pytest

from scripts.run_with_budget import run_with_budget


def test_runtime_budget_preserves_success_and_failure_status() -> None:
    assert run_with_budget([sys.executable, "-c", "pass"], seconds=2) == 0
    assert run_with_budget([sys.executable, "-c", "raise SystemExit(3)"], seconds=2) == 3


def test_runtime_budget_stops_a_slow_command(capsys: pytest.CaptureFixture[str]) -> None:
    status = run_with_budget(
        [sys.executable, "-c", "import time; time.sleep(5)"],
        seconds=0.05,
    )
    assert status == 124
    assert "runtime budget exceeded" in capsys.readouterr().err


@pytest.mark.parametrize("seconds", [0.0, -1.0])
def test_runtime_budget_requires_a_positive_limit(seconds: float) -> None:
    with pytest.raises(ValueError, match="positive"):
        run_with_budget([sys.executable, "-c", "pass"], seconds=seconds)
