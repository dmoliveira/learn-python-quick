"""Run chapter scripts from a temporary directory, outside the repository root."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_EXAMPLES = [
    "chapters/00_start_here/example.py",
    "chapters/01_python_fundamentals/example.py",
    "chapters/02_data_structures_and_iteration/example.py",
    "chapters/03_types_oop_and_pydantic/example.py",
    "chapters/04_files_regex_and_http/example.py",
    "chapters/05_numpy_and_pandas/example.py",
    "chapters/06_ml_workflows_and_metrics/example.py",
    "chapters/07_trees_and_xgboost/example.py",
    "chapters/09_embeddings_and_transformers/example.py",
    "chapters/10_recommenders/example.py",
    "chapters/12_performance_and_quality/example.py",
]
OPTIONAL_EXAMPLES = {
    "boost": ["chapters/07_trees_and_xgboost/xgboost_example.py"],
    "deep": [
        "chapters/08_pytorch_and_images/example.py",
        "chapters/10_recommenders/neural_example.py",
    ],
    "api": ["chapters/11_fastapi_and_mle/example.py"],
}
NETWORK_GUARD = """\
import socket

def denied(*args, **kwargs):
    raise RuntimeError("network disabled by Learn Python Quick smoke runner")

socket.create_connection = denied
socket.socket.connect = denied
"""


def run(
    script: str,
    *,
    working_directory: str,
    environment: dict[str, str],
    timeout: int,
) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=working_directory,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"example failed: {script}")
    print(f"ok  {script}")


def verify_network_guard(*, working_directory: str, environment: dict[str, str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import socket; socket.create_connection(('127.0.0.1', 9), timeout=0.01)",
        ],
        cwd=working_directory,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if "network disabled by Learn Python Quick smoke runner" not in result.stderr:
        raise RuntimeError("the subprocess network guard did not activate")
    print("ok  subprocess sockets are blocked")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--optional", choices=["boost", "deep", "api"])
    args = parser.parse_args()
    scripts = OPTIONAL_EXAMPLES[args.optional] if args.optional else CORE_EXAMPLES
    environment = os.environ.copy()
    environment.update(
        {
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "TOKENIZERS_PARALLELISM": "false",
        }
    )
    with tempfile.TemporaryDirectory(prefix="lpq-examples-") as temporary_directory:
        Path(temporary_directory, "sitecustomize.py").write_text(NETWORK_GUARD, encoding="utf-8")
        existing_python_path = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = temporary_directory + (
            os.pathsep + existing_python_path if existing_python_path else ""
        )
        verify_network_guard(
            working_directory=temporary_directory,
            environment=environment,
        )
        for script in scripts:
            run(
                script,
                working_directory=temporary_directory,
                environment=environment,
                timeout=90 if args.optional else 45,
            )
    print(f"{len(scripts)} example(s) passed outside the repository root with sockets blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
