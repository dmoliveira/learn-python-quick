from __future__ import annotations

from pathlib import Path

import pytest

from scripts.check_exercise import find_exercise, run_exercise

ROOT = Path(__file__).resolve().parents[1]


def make_exercise(root: Path, answer: str, test: str) -> None:
    directory = root / "exercises/easy/01_demo"
    directory.mkdir(parents=True)
    (directory / "answer.py").write_text(answer, encoding="utf-8")
    (directory / "test_answer.py").write_text(test, encoding="utf-8")


def test_runner_reports_a_passing_contract(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_exercise(
        tmp_path,
        "def solve():\n    return 42\n",
        "from answer import solve\n\ndef test_answer():\n    assert solve() == 42\n",
    )
    assert run_exercise("easy/01_demo", root=tmp_path) == 0
    assert "passes its public contract" in capsys.readouterr().out


def test_runner_explains_an_untouched_starter(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_exercise(
        tmp_path,
        'def solve():\n    raise NotImplementedError("implement me")\n',
        "from answer import solve\n\ndef test_answer():\n    solve()\n",
    )
    assert run_exercise("easy/01_demo", root=tmp_path) == 1
    output = capsys.readouterr().out
    assert "expected first result" in output
    assert "Function: solve" in output
    assert "exercise-verbose" in output
    assert "Traceback" not in output


def test_runner_preserves_an_ordinary_failure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    make_exercise(
        tmp_path,
        "def solve():\n    return 1\n",
        "from answer import solve\n\ndef test_answer():\n    assert solve() == 2\n",
    )
    assert run_exercise("easy/01_demo", root=tmp_path) == 1
    output = capsys.readouterr().out
    assert "assert 1 == 2" in output
    assert "not passing yet" in output


def test_verbose_runner_preserves_failure_status(tmp_path: Path) -> None:
    make_exercise(
        tmp_path,
        "def solve():\n    return 1\n",
        "from answer import solve\n\ndef test_answer():\n    assert solve() == 2\n",
    )
    assert run_exercise("easy/01_demo", root=tmp_path, verbose=True) == 1


@pytest.mark.parametrize("identifier", ["../secret", "easy/demo", "expert/01_demo"])
def test_runner_rejects_malformed_or_traversal_ids(
    identifier: str,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert run_exercise(identifier, root=tmp_path) == 2
    assert "Exercise error" in capsys.readouterr().err


def test_runner_rejects_unknown_and_missing_tests(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert run_exercise("easy/01_unknown", root=tmp_path) == 2
    make_exercise(tmp_path, "def solve():\n    return 1\n", "")
    (tmp_path / "exercises/easy/01_demo/test_answer.py").unlink()
    assert run_exercise("easy/01_demo", root=tmp_path) == 2
    assert "Exercise error" in capsys.readouterr().err


def test_runner_rejects_a_symlink_escape(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "answer.py").write_text("def solve(): return 1\n", encoding="utf-8")
    (outside / "test_answer.py").write_text("def test_answer(): pass\n", encoding="utf-8")
    exercise_root = tmp_path / "exercises/easy"
    exercise_root.mkdir(parents=True)
    (exercise_root / "01_escape").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="inside exercises"):
        find_exercise("easy/01_escape", root=tmp_path)


def test_real_starter_gets_concise_expected_guidance(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert run_exercise("easy/01_sales_summary", root=ROOT) == 1
    output = capsys.readouterr().out
    assert "expected first result" in output
    assert "exercises/easy/01_sales_summary/answer.py" in output
