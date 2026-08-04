"""Check local documentation links and curriculum structure without network access."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"\[[^]]*]\(([^)]+)\)")
REQUIRED_CHAPTER_HEADINGS = {"## Outcomes", "## Run it", "## Try it", "## References"}


def local_link_failures() -> list[str]:
    failures: list[str] = []
    for document in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in document.relative_to(ROOT).parts):
            continue
        for raw_target in LINK_PATTERN.findall(document.read_text(encoding="utf-8")):
            target = raw_target.strip().split(maxsplit=1)[0]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = unquote(target.split("#", maxsplit=1)[0])
            if path_part and not (document.parent / path_part).resolve().exists():
                failures.append(f"{document.relative_to(ROOT)} -> {target}")
    return failures


def chapter_failures() -> list[str]:
    failures: list[str] = []
    chapters = sorted((ROOT / "chapters").glob("[0-9][0-9]_*"))
    if len(chapters) != 13:
        failures.append(f"expected 13 chapter directories, found {len(chapters)}")
    for chapter in chapters:
        readme = chapter / "README.md"
        example = chapter / "example.py"
        if not readme.exists() or not example.exists():
            failures.append(f"{chapter.name} needs README.md and example.py")
            continue
        text = readme.read_text(encoding="utf-8")
        missing = REQUIRED_CHAPTER_HEADINGS - set(text.splitlines())
        if missing:
            failures.append(f"{chapter.name} missing headings: {sorted(missing)}")
    return failures


def dataset_failures() -> list[str]:
    manifest_path = ROOT / "datasets/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures: list[str] = []
    for dataset in manifest["datasets"]:
        required = {"id", "purpose", "source", "terms", "network_required", "redistributed"}
        missing = required - set(dataset)
        if missing:
            failures.append(f"dataset {dataset.get('id', '<unknown>')} missing {sorted(missing)}")
        for relative_path, expected in dataset.get("sha256", {}).items():
            path = ROOT / relative_path
            if not path.exists():
                failures.append(f"missing dataset fixture: {relative_path}")
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                failures.append(f"checksum differs: {relative_path}")
    return failures


def exercise_failures() -> list[str]:
    failures: list[str] = []
    exercise_dirs = sorted((ROOT / "exercises").glob("*/*_*"))
    if len(exercise_dirs) != 10:
        failures.append(f"expected 10 exercises, found {len(exercise_dirs)}")
    for exercise in exercise_dirs:
        for name in ("README.md", "answer.py", "test_answer.py"):
            if not (exercise / name).exists():
                failures.append(f"{exercise.relative_to(ROOT)} missing {name}")
    return failures


def main() -> int:
    failures = [
        *local_link_failures(),
        *chapter_failures(),
        *dataset_failures(),
        *exercise_failures(),
    ]
    if not (ROOT / "assets/hero.svg").exists():
        failures.append("missing accessible local hero asset")
    if failures:
        print("Documentation checks failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    markdown_count = len(list(ROOT.rglob("*.md")))
    print(
        f"documentation is consistent: {markdown_count} Markdown files, 13 chapters, 10 exercises"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
