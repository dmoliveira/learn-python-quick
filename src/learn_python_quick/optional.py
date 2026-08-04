"""Consistent errors for isolated optional integrations."""

from __future__ import annotations

import importlib
from types import ModuleType


class OptionalDependencyError(ImportError):
    """An optional chapter was used without installing its dependency group."""


def require_module(module_name: str, *, extra: str) -> ModuleType:
    """Import an optional module or show commands for repository and package users."""
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as error:
        if error.name != module_name:
            raise
        message = (
            f"Optional dependency {module_name!r} is required. "
            f"In this repository run `uv sync --dev --extra {extra}`; "
            f'for an installed package run `pip install "learn-python-quick[{extra}]"`.'
        )
        raise OptionalDependencyError(message) from error
