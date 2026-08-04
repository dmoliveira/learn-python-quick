"""Safe text, file, regex, JSONL, and HTTP examples."""

from __future__ import annotations

import json
import re
from collections.abc import Iterator, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol, cast

import requests

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+"
    r"(?P<level>INFO|WARNING|ERROR|CRITICAL)\s+"
    r"(?P<service>[a-z][a-z0-9_-]*)\s+"
    r"(?P<message>.+)$"
)


class InvalidLogLine(ValueError):
    """Raised when a line does not match the documented log contract."""


@dataclass(frozen=True, slots=True)
class LogEvent:
    timestamp: str
    level: str
    service: str
    message: str


class ResponseLike(Protocol):
    def raise_for_status(self) -> None: ...

    def json(self) -> object: ...


class SessionLike(Protocol):
    def get(self, url: str, *, timeout: float) -> ResponseLike: ...


def parse_log_line(line: str) -> LogEvent:
    """Parse one strict, machine-readable log line."""
    match = LOG_PATTERN.fullmatch(line.strip())
    if match is None:
        raise InvalidLogLine(f"invalid log line: {line!r}")
    return LogEvent(**match.groupdict())


def incident_events(lines: Iterator[str]) -> tuple[list[LogEvent], int]:
    """Return error events and the count of malformed non-empty lines."""
    incidents: list[LogEvent] = []
    invalid_count = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_log_line(line)
        except InvalidLogLine:
            invalid_count += 1
            continue
        if event.level in {"ERROR", "CRITICAL"}:
            incidents.append(event)
    return incidents, invalid_count


def write_jsonl(events: Iterator[LogEvent], path: str | Path) -> None:
    """Write one JSON object per line using a context manager."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as stream:
        for event in events:
            stream.write(json.dumps(asdict(event), sort_keys=True) + "\n")


def read_jsonl(path: str | Path) -> Iterator[dict[str, object]]:
    """Stream JSONL records and include line context in parsing failures."""
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            try:
                value: object = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSON on line {line_number}") from error
            if not isinstance(value, dict):
                raise ValueError(f"line {line_number} must contain a JSON object")
            yield cast(dict[str, object], value)


def fetch_json(
    url: str,
    *,
    session: SessionLike | None = None,
    timeout: float = 5.0,
) -> Mapping[str, object]:
    """Fetch one JSON object with an explicit timeout and injectable transport."""
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    client: SessionLike = session if session is not None else cast(SessionLike, requests.Session())
    response = client.get(url, timeout=timeout)
    response.raise_for_status()
    value = response.json()
    if not isinstance(value, dict):
        raise ValueError("expected the response to contain a JSON object")
    return cast(dict[str, object], value)
