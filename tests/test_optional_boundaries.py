from __future__ import annotations

import importlib
import sys

import pytest

from learn_python_quick.optional import OptionalDependencyError, require_module


def test_core_import_does_not_import_optional_libraries() -> None:
    import learn_python_quick

    assert learn_python_quick.__version__ == "0.1.0"
    assert "torch" not in sys.modules
    assert "xgboost" not in sys.modules
    assert "fastapi" not in sys.modules


def test_missing_optional_error_gives_uv_and_pip_commands(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_import = importlib.import_module

    def missing(name: str) -> object:
        if name == "invented_optional_library":
            error = ModuleNotFoundError(name)
            error.name = name
            raise error
        return real_import(name)

    monkeypatch.setattr(importlib, "import_module", missing)
    with pytest.raises(OptionalDependencyError) as captured:
        require_module("invented_optional_library", extra="deep")
    message = str(captured.value)
    assert "uv sync --dev --extra deep" in message
    assert 'pip install "learn-python-quick[deep]"' in message
