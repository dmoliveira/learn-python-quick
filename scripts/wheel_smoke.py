"""Install the built wheel in a clean venv and run code outside the checkout."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def checked(command: list[str], *, cwd: str | Path | None = None) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=cwd, check=True, timeout=180)


def main() -> int:
    wheels = sorted((ROOT / "dist").glob("learn_python_quick-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError("run `make build` first; expected exactly one wheel in dist/")
    uv = os.environ.get("UV", "uv")
    with tempfile.TemporaryDirectory(prefix="lpq-wheel-") as temporary_directory:
        temporary = Path(temporary_directory)
        environment = temporary / "venv"
        checked([uv, "venv", "--python", "3.12", str(environment)])
        python = environment / "bin/python"
        checked([uv, "pip", "install", "--python", str(python), str(wheels[0])])
        checked(
            [
                str(python),
                "-c",
                "import learn_python_quick; print(learn_python_quick.__version__)",
            ],
            cwd=temporary,
        )
        checked([str(python), str(ROOT / "chapters/00_start_here/example.py")], cwd=temporary)
    print("wheel installs and runs outside the repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
