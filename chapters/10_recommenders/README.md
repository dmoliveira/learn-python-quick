# 10 · Recommenders 🎬

**Time:** 65 minutes · **Prerequisites:** [Metrics](../06_ml_workflows_and_metrics/README.md) and
[embeddings](../09_embeddings_and_transformers/README.md)

## Outcomes

You will be able to:

- distinguish explicit ratings from implicit interaction signals;
- build popularity and unseen-item baselines;
- explain collaborative filtering and user/item embeddings;
- use temporal evaluation with Precision@K and Recall@K;
- identify cold-start, feedback-loop, and exposure problems.

## Start simple

A popularity model is easy to understand, hard to break, and a strong baseline. Exclude items the
user already consumed when the product needs discovery. Define deterministic tie-breaking so tests
and user experience remain stable.

Collaborative filtering learns from patterns across users and items. Matrix factorization assigns
each user and item a vector; their dot product estimates affinity. A neural recommender can learn the
same embeddings with gradient descent and add nonlinear features, but complexity does not solve poor
labels or biased exposure.

## Evaluate the ranking

Randomly hiding interactions can leak future behavior. Prefer a temporal split: train on earlier
events and ask whether the model retrieves later relevant items. State:

- what counts as a relevant interaction;
- which items are candidates;
- why each ranked item ID is unique;
- cutoff `K`;
- treatment of unknown users/items;
- comparison against popularity and random baselines.

Offline ranking gains may not improve satisfaction. Real systems also consider diversity, novelty,
latency, safety, business constraints, and online experiments.

## Run it

Core popularity baseline:

```bash
uv run python chapters/10_recommenders/example.py
```

Optional tiny embedding model:

```bash
uv sync --dev --extra deep
uv run python chapters/10_recommenders/neural_example.py
```

## Try it

- Add a brand-new user and define a sensible fallback.
- Compare Precision@2 when relevant items contain one versus four items.
- Split the generated interactions by an added timestamp.
- Solve [Recommend unseen items](../../exercises/hard/06_recommender/README.md).

## References

- [Google ML recommendation overview](https://developers.google.com/machine-learning/recommendation)
- [NDCG definition in scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html)
- [MovieLens datasets and terms](https://grouplens.org/datasets/movielens/)
- [Local metrics guide](../../docs/metrics.md#retrieval-and-recommenders)
