"""Round-trip JSONL and preserve line context for malformed records."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from learn_python_quick.text_io import LogEvent, read_jsonl, write_jsonl


def main() -> None:
    events = iter(
        [
            LogEvent("2026-08-04T09:00:00Z", "ERROR", "payments", "timeout"),
            LogEvent("2026-08-04T09:02:00Z", "CRITICAL", "checkout", "database down"),
        ]
    )

    with TemporaryDirectory(prefix="lpq-jsonl-") as directory:
        path = Path(directory) / "incidents.jsonl"
        write_jsonl(events, path)
        records = list(read_jsonl(path))
        print(f"valid records={len(records)} services={[row['service'] for row in records]}")

        with path.open("a", encoding="utf-8") as stream:
            stream.write("not-json\n")
        try:
            list(read_jsonl(path))
        except ValueError as error:
            print(f"quality check preserved context: {error}")


if __name__ == "__main__":
    main()
