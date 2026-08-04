# Contributing

Thank you for helping people learn. Keep changes small, clear, and runnable.

## Start

1. Fork the repository and create a focused branch.
2. Run `uv sync --dev` (or `make setup-all` for optional integrations).
3. Run `make check` before and after your change.
4. Open a pull request that explains the learner problem and the validation you ran.

## Add or change course content

- Write in simple English. Prefer short sentences and concrete examples.
- Give a chapter explicit outcomes, prerequisites, a runnable command, and primary references.
- Give an exercise expected time, input/output examples, edge cases, and one focused contract.
- Test the official solution against the same public contract used by learners.
- Keep default examples offline. Document any optional network access before adding it.
- Add every new dataset to `datasets/manifest.json` with its source and usage terms.

## Quality gates

```bash
make check
make wheel-smoke
git diff --check
```

Changes to `boosting.py`, `deep_learning.py`, or `api.py` also require the matching tests under
`tests/optional/`. Never add an optional import to `learn_python_quick/__init__.py`.

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
