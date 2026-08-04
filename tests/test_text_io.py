from __future__ import annotations

from pathlib import Path

import pytest

from learn_python_quick.text_io import (
    InvalidLogLine,
    LogEvent,
    ResponseLike,
    fetch_json,
    incident_events,
    parse_log_line,
    read_jsonl,
    write_jsonl,
)


class FakeResponse(ResponseLike):
    def __init__(self, payload: object) -> None:
        self.payload = payload
        self.checked = False

    def raise_for_status(self) -> None:
        self.checked = True

    def json(self) -> object:
        assert self.checked
        return self.payload


class FakeSession:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.timeout: float | None = None

    def get(self, url: str, *, timeout: float) -> ResponseLike:
        assert url.startswith("https://")
        self.timeout = timeout
        return self.response


def test_parse_and_filter_log_events() -> None:
    event = parse_log_line("2026-08-04T09:00:00Z ERROR api timed out")
    assert event.service == "api"
    incidents, invalid = incident_events(
        iter(["2026-08-04T09:00:00Z INFO api ok", "bad", "", str(event)])
    )
    assert incidents == []
    assert invalid == 2  # dataclass repr is not a valid machine log line
    with pytest.raises(InvalidLogLine):
        parse_log_line("missing fields")


def test_jsonl_round_trip_and_context(tmp_path: Path) -> None:
    path = tmp_path / "nested/events.jsonl"
    events = iter([LogEvent("2026-08-04T09:00:00Z", "ERROR", "api", "timeout")])
    write_jsonl(events, path)
    assert list(read_jsonl(path)) == [
        {
            "level": "ERROR",
            "message": "timeout",
            "service": "api",
            "timestamp": "2026-08-04T09:00:00Z",
        }
    ]
    path.write_text("{}\nnot-json\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 2"):
        list(read_jsonl(path))


def test_fetch_json_uses_injected_transport_and_timeout() -> None:
    response = FakeResponse({"ok": True})
    session = FakeSession(response)
    assert fetch_json("https://example.invalid", session=session, timeout=1.5) == {"ok": True}
    assert session.timeout == 1.5
    with pytest.raises(ValueError, match="JSON object"):
        fetch_json(
            "https://example.invalid",
            session=FakeSession(FakeResponse([1, 2])),
        )
