# Exercise guide

## The workflow

1. Read the linked chapters and references in the exercise README.
2. Inspect its fixture and example output.
3. Run `make exercise ID=<level>/<name>` once to see the contract fail.
4. Change only that exercise's `answer.py`.
5. Run the check after each small step.
6. Explain your choices before opening the solution.

Learner tests are public feedback, not hidden assessment. A passing test is evidence for listed
cases, not proof that code is correct for every possible input.

## Difficulty

| Level | Typical time | Shape |
|---|---:|---|
| 🟢 Easy | 15–30 min | One main idea and a few edge cases |
| 🟡 Medium | 40–75 min | Several transformations or metrics |
| 🔴 Hard | 90–180 min | Design choices, library APIs, and trade-offs |

If you are stuck for 20 minutes, reread the hints and run a tiny input in a one-line Python command.
Then inspect the relevant official documentation. Read the solution only after writing down what is
unclear.

## What to explain

For medium and hard problems, add brief comments or notes answering:

- What assumptions does the function make?
- What happens with empty, missing, or invalid input?
- Why does the selected metric fit the product decision?
- Where could data leakage or unfairness enter?
- What would change for ten million rows or real traffic?

## Challenge catalog

These follow-ups reuse chapter code. They intentionally have no default test so the core path stays
small. Start by writing your own contract, then compare with the chapter example.

| Challenge | Starting point | Definition of done |
|---|---|---|
| Tune boosted trees | [Chapter 07](../chapters/07_trees_and_xgboost/README.md) | Compare baseline/XGBoost with cross-validation and justify one parameter |
| Improve the digits MLP | [Chapter 08](../chapters/08_pytorch_and_images/README.md) | Beat the stated baseline without using test data for tuning |
| Build semantic search | [Chapter 09](../chapters/09_embeddings_and_transformers/README.md) | Return relevant top-3 text and report Recall@3 on labeled queries |
| Train a neural recommender | [Chapter 10](../chapters/10_recommenders/README.md) | Compare it with popularity using the same temporal split |
| Add API batch prediction | [Chapter 11](../chapters/11_fastapi_and_mle/README.md) | Validate 1–100 rows and test 200/422 responses in process |
| Profile a slow feature step | [Chapter 12](../chapters/12_performance_and_quality/README.md) | Measure before/after and report time plus memory trade-off |
