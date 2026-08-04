.DEFAULT_GOAL := help

ID ?=

.PHONY: help setup setup-all format lint typecheck test test-solutions test-optional _test-optional test-all docs examples check _check build wheel-smoke exercise exercise-verbose clean

help: ## Show the available commands.
	@awk 'BEGIN {FS = ":.*## "; printf "\nLearn Python Quick\n\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Install the core course and development tools.
	uv sync --dev

setup-all: ## Install core plus XGBoost, PyTorch, and FastAPI extras.
	uv sync --dev --all-extras

format: ## Format Python files with Ruff.
	uv run ruff format .
	uv run ruff check --fix .

lint: ## Check formatting and lint rules.
	uv run ruff format --check .
	uv run ruff check .

typecheck: ## Type-check the reusable package.
	uv run mypy src

test: ## Run the always-green core repository tests.
	uv run pytest tests --ignore=tests/optional

test-solutions: ## Validate every official exercise solution.
	uv run pytest tests/solutions

test-optional: ## Run optional tests and examples under 3 minutes (requires setup-all).
	uv run python scripts/run_with_budget.py 180 $(MAKE) _test-optional

_test-optional:
	uv run pytest tests/optional
	uv run python scripts/smoke_examples.py --optional boost
	uv run python scripts/smoke_examples.py --optional deep
	uv run python scripts/smoke_examples.py --optional api

test-all: ## Run core and optional tests.
	uv run pytest tests

docs: ## Check local links, chapter shape, and dataset metadata.
	uv run python scripts/check_docs.py

examples: ## Run core chapter examples from an outside directory.
	uv run python scripts/smoke_examples.py

check: ## Run the offline-default gate under 60 seconds.
	uv run python scripts/run_with_budget.py 60 $(MAKE) _check

_check: lint typecheck test docs examples

build: ## Build wheel and source distributions.
	rm -rf dist
	uv build

wheel-smoke: build ## Install the wheel in a clean environment and smoke-test it.
	uv run python scripts/wheel_smoke.py

exercise: ## Check one learner answer: make exercise ID=easy/01_sales_summary
	@test -n "$(ID)" || (echo "Use: make exercise ID=easy/01_sales_summary" && exit 2)
	uv run python scripts/check_exercise.py "$(ID)"

exercise-verbose: ## Show full pytest output for one learner answer.
	@test -n "$(ID)" || (echo "Use: make exercise-verbose ID=easy/01_sales_summary" && exit 2)
	uv run python scripts/check_exercise.py "$(ID)" --verbose

clean: ## Remove generated caches and build output.
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache build dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
