"""Run one learner exercise with concise, non-spoiling feedback."""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXERCISE_ID = re.compile(r"^(easy|medium|hard)/[0-9]{2}_[a-z0-9_]+$")


class ExerciseLookupError(ValueError):
    """Raised when an exercise ID does not resolve to a safe course path."""


@dataclass(frozen=True, slots=True)
class Exercise:
    identifier: str
    directory: Path
    answer: Path
    test: Path


def find_exercise(identifier: str, *, root: Path = ROOT) -> Exercise:
    """Resolve a documented ID without allowing paths outside ``exercises``."""
    if EXERCISE_ID.fullmatch(identifier) is None:
        raise ExerciseLookupError("exercise ID must look like easy/01_sales_summary")

    exercises_root = (root / "exercises").resolve()
    candidate = exercises_root.joinpath(*identifier.split("/"))
    directory = candidate.resolve()
    if not directory.is_relative_to(exercises_root):
        raise ExerciseLookupError("exercise path must stay inside exercises/")
    if not directory.is_dir():
        raise ExerciseLookupError(f"unknown exercise: {identifier}")

    answer = directory / "answer.py"
    test = directory / "test_answer.py"
    for path in (answer, test):
        if not path.is_file() or not path.resolve().is_relative_to(exercises_root):
            raise ExerciseLookupError(f"exercise is missing a safe {path.name}")
    return Exercise(identifier, directory, answer, test)


def target_function(answer: Path) -> str:
    """Find the first public function name without importing learner code."""
    try:
        tree = ast.parse(answer.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return "the target function"
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            return node.name
    return "the target function"


def run_exercise(
    identifier: str,
    *,
    verbose: bool = False,
    root: Path = ROOT,
) -> int:
    """Run pytest and preserve its success or failure status."""
    try:
        exercise = find_exercise(identifier, root=root)
    except ExerciseLookupError as error:
        print(f"Exercise error: {error}", file=sys.stderr)
        print("Use: make exercise ID=easy/01_sales_summary", file=sys.stderr)
        return 2

    command = [sys.executable, "-m", "pytest", str(exercise.test)]
    if verbose:
        return subprocess.run([*command, "-vv"], cwd=root, check=False).returncode

    result = subprocess.run(
        [*command, "-q", "--tb=line"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())
    answer_source = exercise.answer.read_text(encoding="utf-8")

    if result.returncode == 0:
        print(f"✓ {identifier} passes its public contract.")
        print("Next: explain your edge-case choices before reading the solution.")
        return 0

    if (
        result.returncode == 1
        and "NotImplementedError" in output
        and "NotImplementedError" in answer_source
    ):
        print("Not solved yet — this is the expected first result.")
        print(f"Edit: {exercise.answer.relative_to(root)}")
        print(f"Function: {target_function(exercise.answer)}")
        print("The starter still raises NotImplementedError.")
    else:
        print(output)
        print(f"\n{identifier} is not passing yet.")
        print(f"Edit: {exercise.answer.relative_to(root)}")

    print(f"Rerun: make exercise ID={identifier}")
    print(f"Full details: make exercise-verbose ID={identifier}")
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exercise_id", help="for example: easy/01_sales_summary")
    parser.add_argument("--verbose", action="store_true", help="show normal pytest output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run_exercise(args.exercise_id, verbose=args.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
