# 06 · Recommend unseen items 🎁

**Level:** 🔴 Hard · **Time:** 75–100 min · **Read first:**
[Data structures](../../../chapters/02_data_structures_and_iteration/README.md),
[metrics](../../../chapters/06_ml_workflows_and_metrics/README.md), and
[recommenders](../../../chapters/10_recommenders/README.md)

## Problem

An interaction is `(user_id, item_id)`. Implement
`recommend_unseen(interactions, *, user_id, k)` in [`answer.py`](answer.py).

Build a transparent popularity baseline:

1. count every positive interaction per item;
2. remove items already seen by the requested user;
3. rank by descending count, then alphabetically for ties;
4. return at most `k` item IDs.

### Contract

- `k` must be at least 1 or raise `ValueError`.
- An unknown user has seen nothing and receives the global ranking.
- Repeated interactions count repeatedly; state why that may be wrong for another product.
- If fewer than `k` candidates exist, return all candidates.
- Do not mutate the input.

Try [`interactions.csv`](../../../datasets/generated/interactions.csv), then define one future item as
relevant and calculate Precision@K.

## Design before code

Use a `Counter` for popularity and a set for seen-item membership. Keep candidate generation separate
from sorting. Estimate the complexity in users, interactions, and unique items.

This baseline favors already popular items and cannot personalize unknown users. That is useful as a
comparison, not a fairness or discovery strategy.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=hard/06_recommender
```

Before opening the answer, explain the cold-start fallback and tie rule.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#06--recommend-unseen-items), then inspect
[`recommender.py`](../../../solutions/hard/recommender.py).

</details>
