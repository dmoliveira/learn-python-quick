# Learning datasets

Read the human-friendly [dataset guide](../docs/datasets.md) and the machine-readable
[`manifest.json`](manifest.json) before adding or redistributing data.

Recreate the tiny committed fixtures with:

```bash
uv run python datasets/generate.py --write
uv run python datasets/generate.py --check
```

Core model examples call scikit-learn `load_*` functions. They never call a network-backed
`fetch_*` loader.
