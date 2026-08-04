"""Reproduce the tiny exercise fixtures byte for byte."""

from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GENERATED = ROOT / "generated"


def csv_bytes(header: list[str], rows: list[list[object]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode()


FILES: dict[str, bytes] = {
    "sales.csv": csv_bytes(
        ["product", "units", "unit_price"],
        [
            ["coffee", 2, "4.50"],
            ["tea", 3, "3.25"],
            ["coffee", 1, "4.50"],
            ["cake", 2, "5.75"],
            ["tea", 2, "3.25"],
        ],
    ),
    "incidents.log": (
        b"2026-08-04T09:00:00Z INFO checkout request-complete\n"
        b"2026-08-04T09:01:12Z ERROR payments card-provider-timeout\n"
        b"not-a-valid-log-line\n"
        b"2026-08-04T09:04:31Z WARNING search latency-high\n"
        b"2026-08-04T09:05:10Z CRITICAL checkout database-unavailable\n"
    ),
    "customer_events.csv": csv_bytes(
        ["customer_id", "event", "amount", "occurred_at"],
        [
            ["c-001", "purchase", "29.90", "2026-07-01T10:00:00Z"],
            ["c-002", "support", "0.00", "2026-07-01T11:30:00Z"],
            ["c-001", "purchase", "12.50", "2026-07-03T09:00:00Z"],
            ["c-003", "visit", "0.00", "2026-07-03T12:15:00Z"],
            ["c-002", "purchase", "7.00", "2026-07-04T14:00:00Z"],
            ["c-001", "support", "0.00", "2026-07-05T08:45:00Z"],
        ],
    ),
    "interactions.csv": csv_bytes(
        ["user_id", "item_id", "rating"],
        [
            ["u1", "python-book", 1],
            ["u1", "ml-course", 1],
            ["u2", "python-book", 1],
            ["u2", "data-course", 1],
            ["u2", "ml-course", 1],
            ["u3", "data-course", 1],
            ["u3", "systems-book", 1],
            ["u4", "python-book", 1],
            ["u4", "data-course", 1],
        ],
    ),
}


def write_files() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    for name, content in FILES.items():
        (GENERATED / name).write_bytes(content)
        print(f"wrote datasets/generated/{name}")


def check_files() -> int:
    failures = []
    for name, expected in FILES.items():
        path = GENERATED / name
        if not path.exists() or path.read_bytes() != expected:
            failures.append(name)
    if failures:
        print("fixtures differ; run with --write: " + ", ".join(failures))
        return 1
    print(f"{len(FILES)} generated fixtures are reproducible")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true", help="replace generated fixtures")
    action.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    if args.write:
        write_files()
        return 0
    return check_files()


if __name__ == "__main__":
    raise SystemExit(main())
