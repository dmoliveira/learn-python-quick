from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[2]
STARTERS = {
    "exercises/easy/01_sales_summary/answer.py": ("summarize_sales", ["rows"]),
    "exercises/easy/02_incident_log/answer.py": ("triage_incidents", ["lines"]),
    "exercises/medium/03_customer_features/answer.py": ("build_customer_features", ["events"]),
    "exercises/medium/04_classification_metrics/answer.py": (
        "evaluate_binary_classifier",
        ["y_true", "y_pred"],
    ),
    "exercises/hard/05_risk_pipeline/answer.py": ("build_risk_pipeline", ["seed"]),
    "exercises/hard/06_recommender/answer.py": (
        "recommend_unseen",
        ["interactions", "user_id", "k"],
    ),
}


def load(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"starter_{path.parent.name}", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(("relative_path", "contract"), STARTERS.items())
def test_starter_imports_with_documented_signature(
    relative_path: str,
    contract: tuple[str, list[str]],
) -> None:
    function_name, expected_parameters = contract
    module = load(ROOT / relative_path)
    function = getattr(module, function_name)
    assert callable(function)
    assert list(inspect.signature(function).parameters) == expected_parameters
    assert function.__doc__
