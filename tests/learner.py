"""Load a nearby learner answer without ambiguous global imports."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def load_answer(test_file: str) -> ModuleType:
    path = Path(test_file).with_name("answer.py")
    module_name = "learner_answer_" + "_".join(path.parts[-4:-1])
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
