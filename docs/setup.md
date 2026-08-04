# Setup

## 1. Install uv

[`uv`](https://docs.astral.sh/uv/) manages Python, the virtual environment, and locked dependencies.
Follow its official installation guide, then check:

```bash
uv --version
```

## 2. Install the core course

From the repository root:

```bash
uv sync --dev
uv run python --version
uv run lpq roadmap
make check
```

The project pins Python 3.12 for local work and tests the core on 3.11–3.13. System Python does not
need to match because uv can install a managed interpreter.

## 3. Add only what you need

Heavy libraries are not part of the core path.

| Topic | Command | Used by |
|---|---|---|
| XGBoost | `uv sync --dev --extra boost` | Chapter 07 |
| PyTorch | `uv sync --dev --extra deep` | Chapters 08 and 10 |
| FastAPI | `uv sync --dev --extra api` | Chapter 11 |
| Everything | `uv sync --dev --all-extras` | Optional CI and full exploration |

If this project is installed as a package elsewhere, use
`pip install "learn-python-quick[deep]"` (replace `deep` with the needed extra).

## Useful commands

```bash
make help
make examples
make exercise ID=easy/01_sales_summary
make test-solutions
make wheel-smoke
```

The first exercise check fails until you implement its `answer.py`. `make test` validates repository
code and official solutions, so it remains green with untouched starters.

## Troubleshooting

### `uv` selected the wrong Python

Run `uv python install 3.12`, then `uv sync --python 3.12 --dev`.

### An optional library is missing

Read the error message and install the named extra. Optional code gives both the `uv sync` command
for this repository and the `pip install` command for package users.

### A model result differs slightly

Floating-point operations can vary by platform. Tests use tolerances and metric ranges rather than
bit-for-bit values. PyTorch reproducibility is best effort across different hardware and versions.

### Start clean

```bash
make clean
rm -rf .venv
uv sync --dev
make check
```
