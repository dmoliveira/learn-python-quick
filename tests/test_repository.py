from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generated_fixtures_are_reproducible() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "datasets/generate.py"), "--check"],
        cwd=ROOT,
        check=True,
        timeout=10,
    )


def test_manifest_checksums_match_and_default_data_is_offline() -> None:
    manifest = json.loads((ROOT / "datasets/manifest.json").read_text(encoding="utf-8"))
    for dataset in manifest["datasets"]:
        assert dataset["network_required"] is False
        for relative_path, expected in dataset.get("sha256", {}).items():
            assert hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest() == expected


def test_default_python_examples_do_not_use_download_loaders() -> None:
    paths = [ROOT / "src", ROOT / "chapters"]
    offenders = []
    for base in paths:
        for path in base.rglob("*.py"):
            if "fetch_openml(" in path.read_text(encoding="utf-8"):
                offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []
