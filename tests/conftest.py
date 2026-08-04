from __future__ import annotations

import socket
from collections.abc import Iterator
from typing import NoReturn

import pytest


@pytest.fixture(autouse=True)
def block_unexpected_network(
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> Iterator[None]:
    """Core and optional tests must opt in before opening a real socket."""
    if request.node.get_closest_marker("network") is not None:
        yield
        return

    def denied(*args: object, **kwargs: object) -> NoReturn:
        del args, kwargs
        raise RuntimeError("unexpected network access; inject a fake transport")

    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
    yield
