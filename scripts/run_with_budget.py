"""Run a command with one aggregate wall-time budget."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from collections.abc import Sequence
from time import monotonic


def _stop_process_group(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        os.killpg(process.pid, signal.SIGTERM)
    else:
        process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.wait()


def run_with_budget(command: Sequence[str], *, seconds: float) -> int:
    """Return the command status, or 124 when its aggregate budget expires."""
    if seconds <= 0:
        raise ValueError("seconds must be positive")
    if not command:
        raise ValueError("command must not be empty")

    started = monotonic()
    process = subprocess.Popen(list(command), start_new_session=os.name == "posix")
    try:
        return_code = process.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        _stop_process_group(process)
        elapsed = monotonic() - started
        print(
            f"runtime budget exceeded after {elapsed:.2f}s (limit {seconds:.2f}s): "
            f"{' '.join(command)}",
            file=sys.stderr,
        )
        return 124

    elapsed = monotonic() - started
    print(f"runtime budget: {elapsed:.2f}s / {seconds:.2f}s")
    return return_code


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seconds", type=float, help="Maximum aggregate wall time in seconds")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command and arguments to run")
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command is required")
    return run_with_budget(command, seconds=args.seconds)


if __name__ == "__main__":
    raise SystemExit(main())
