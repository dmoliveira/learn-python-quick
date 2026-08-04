# Contributor and agent guide

This file is the repository's canonical workflow guide.

## Goal

Keep the course friendly, executable, CPU-small, and useful to software engineers moving into
Data Science or Machine Learning Engineering. Prefer one clear example over several clever ones.

## Commands

Run `make help` first. The required fast gate is `make check`; package changes also require
`make wheel-smoke`. Optional integration changes require `make setup-all && make test-optional`.
Use `make exercise ID=<level>/<exercise>` only for a learner answer; untouched starters are
expected to fail their behavioral test.

## Content rules

- Use simple English and define specialist terms before using them.
- Give each chapter outcomes, a runnable example, an exercise link, and primary references.
- Keep default examples offline and deterministic. Never add a hidden download.
- Put reusable behavior in `src/learn_python_quick/`; keep chapter scripts small.
- Keep optional XGBoost, PyTorch, and FastAPI imports out of `learn_python_quick.__init__`.
- Add public contract tests for exercises and test official solutions against the same contract.
- Record source, license/terms, network behavior, and generation details for every dataset.

## Delivery

Use a feature branch and pull request. Run Ruff, mypy, core tests, docs checks, example smoke tests,
and a wheel smoke test before merge. Run the matching optional test whenever an optional module is
changed.
