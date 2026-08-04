"""Small command-line navigation for the course."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from learn_python_quick import __version__

ROADMAP: tuple[tuple[str, str], ...] = (
    ("01-04", "Modern Python: functions, collections, types, files, regex, and HTTP"),
    ("05-07", "Data Science: NumPy, pandas, metrics, pipelines, trees, and XGBoost"),
    ("08-12", "MLE: PyTorch, embeddings, recommenders, APIs, and performance"),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lpq",
        description="Navigate the Learn Python Quick curriculum.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("roadmap", help="Show the three curriculum stages.")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Run the course navigation CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "roadmap":
        parser.print_help()
        return

    print("Learn Python Quick roadmap\n")
    print("  Start: Chapter 00 teaches the run-change-test learning loop.\n")
    for chapters, outcome in ROADMAP:
        print(f"  Chapters {chapters}: {outcome}")
    print("\nNext: open chapters/00_start_here/README.md")
    print("Track: docs/learning-paths.md#my-progress")
