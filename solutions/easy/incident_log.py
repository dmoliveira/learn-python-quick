"""Solution: parse the full log contract, then filter incident levels."""

from __future__ import annotations

import re

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+"
    r"(?P<level>INFO|WARNING|ERROR|CRITICAL)\s+"
    r"(?P<service>[a-z][a-z0-9_-]*)\s+"
    r"(?P<message>.+)$"
)


def triage_incidents(lines: list[str]) -> dict[str, object]:
    incidents: list[dict[str, str]] = []
    invalid_lines = 0

    for line in lines:
        if not line.strip():
            continue
        match = LOG_PATTERN.fullmatch(line.strip())
        if match is None:
            invalid_lines += 1
            continue
        event = match.groupdict()
        if event["level"] in {"ERROR", "CRITICAL"}:
            incidents.append(event)

    return {"incidents": incidents, "invalid_lines": invalid_lines}
