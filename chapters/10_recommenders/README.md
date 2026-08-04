# 10 · Recommenders 🎬

**Time:** 65 minutes · **Prerequisites:** [Metrics](../06_ml_workflows_and_metrics/README.md) and
[embeddings](../09_embeddings_and_transformers/README.md)

## Outcomes

You will be able to:

- distinguish explicit ratings from implicit interaction and exposure signals;
- build popularity and unseen-item baselines;
- explain collaborative filtering and user/item embeddings;
- use temporal evaluation with Precision@K and Recall@K;
- define candidates, relevance, and unknown-user behavior;
- identify cold-start, feedback-loop, and exposure problems.

## Recommendation is ranking under constraints

A recommender ranks eligible items for a user or context. The output is not simply “items the user
likes”; it depends on what was available, what was shown, what the user did, and what the product is
allowed to show now.

```text
eligible candidates → score → filter/rerank → top K → exposure → interaction → future training data
```

That last arrow creates a feedback loop. The model sees labels mostly for items previous systems
exposed, not for every item the user might have liked.

## Signals do not all mean preference

- **Explicit feedback:** ratings, likes, or survey answers directly express a response, but are often
  sparse and selected by highly engaged users.
- **Implicit feedback:** clicks, views, purchases, completion, or dwell time is abundant but mixes
  preference with position, availability, price, interface, and accidental actions.
- **Exposure:** an item was eligible and shown. Without exposure data, a missing click cannot cleanly
  mean dislike.
- **Negative feedback:** hide/report/dislike can be stronger but has its own product meaning.

Write down the event, value, time, and attribution window. Repeated plays may indicate preference or
simply autoplay. A purchase may be a gift. Domain review belongs before algorithm selection.

## Start with a deterministic popularity baseline

A popularity model counts positive interactions in training data and sorts by count. It is easy to
understand, cheap to serve, and a strong fallback for unknown users.

```text
rank key = (-positive_interaction_count, item_id)
```

The item ID tie-break makes output stable. When the product goal is discovery, remove items already
consumed by the user. Also apply current eligibility rules: inventory, region, age/safety restrictions,
and business rules should not be left to the scoring model.

The baseline exposes evaluation mistakes. If a complex model cannot beat popularity on the same
temporal split and candidates, complexity has not earned its operational cost.

## Define candidate and relevant sets

For each evaluation user, state:

- **training history:** interactions available before the cutoff;
- **seen set:** items that should be excluded from discovery recommendations;
- **candidate set:** items the model could actually rank at prediction time;
- **relevant set:** held-out future items that count as success;
- **K:** number of positions the interface will show;
- **fallback:** behavior for unknown users or too few eligible items.

Future items unknown to the training catalog cannot be ranked by a pure popularity model. Silently
including them as candidates penalizes that baseline for an impossible task; silently excluding hard
known candidates can make every model look too good. Candidate construction is part of the metric.

## Time usually defines the honest split

Randomly hiding interactions can let future popularity and later user behavior influence training.
Prefer a global or per-user temporal cutoff when deployment ranks future items:

```text
training interactions: occurred_at < cutoff
held-out relevance:    occurred_at >= cutoff and item was eligible
```

Use strict timezone-aware timestamps and document how events exactly at the cutoff are handled.
Deduplicate repeated events according to product meaning before splitting. Fit every count, embedding,
and candidate statistic using training data only.

## Ranking metrics have denominator choices

At cutoff `K`:

- **Precision@K** divides relevant results in the first K by K. It asks how much visible space was
  useful, even if fewer than K items were returned.
- **Recall@K** divides retrieved relevant items by the size of the known relevant set.
- **MRR** rewards placing the first relevant item early.
- **NDCG@K** discounts lower ranks and can support graded relevance.

Report user count and eligible/relevant counts with metric averages. Decide whether users with no
held-out relevant item are excluded, assigned zero, or handled by a separate coverage report. A macro
average gives each user equal weight; a micro calculation can let heavy users dominate.

Offline gains do not prove better satisfaction. A ranking may increase clicks while reducing novelty,
diversity, fairness, trust, or long-term value. Online experiments need guardrail metrics and a clear
intervention, not only a click-through target.

## Worked problem: one temporal cutoff

The core example uses `2026-07-10T00:00:00Z` as a global cutoff. It builds popularity only from earlier
rows, then asks whether the ranking finds `u1`'s later, previously unseen `ml-course` event. The same
item appears in another user's earlier activity, so it is a valid known candidate without future
leakage.

```bash
uv run python chapters/10_recommenders/example.py
```

The generated interaction fixture is small and deterministic. Its generation process, terms, and
network behavior are recorded in the [dataset manifest](../../datasets/manifest.json). It is designed
to demonstrate evaluation boundaries, not estimate real user behavior.

## Collaborative filtering shares information

Collaborative filtering uses interaction patterns across users and items. Matrix factorization gives
each user and item a learned vector; their dot product estimates affinity:

```text
score(user, item) = user_embedding · item_embedding + optional biases
```

Training implicit feedback requires choices about unobserved pairs. Treating every missing interaction
as a confident negative overwhelms positives and ignores exposure. Common systems sample negatives or
weight observed/unobserved pairs, but that sampling distribution becomes part of the objective.

Embedding width, regularization, sampling, and training epochs are validation choices. User/item IDs
are lookup keys, not meaningful numeric quantities. Unknown IDs need a fallback or feature-based
representation.

## Optional neural example

The optional example learns tiny user and item embeddings with PyTorch and ranks unseen items:

```bash
uv sync --dev --extra deep
uv run python chapters/10_recommenders/neural_example.py
```

It constructs all user-item pairs because the local fixture is tiny. Real catalogs need deliberate
negative sampling, batching, approximate retrieval, and resource budgets. Do not compare its printed
items with the popularity output as a general quality claim; use the same temporal labels and metrics.

## Cold start and changing catalogs

- **New user:** use popularity/context, ask for preferences, or use session features.
- **New item:** use item metadata/content, exploration, or editorial placement.
- **Sparse user:** blend a personal score with a robust baseline.
- **Changing catalog:** version eligibility and refresh indexes/counts without mixing future events.

Exploration can collect information about less-exposed items, but it spends user attention and may
have safety/business costs. Define bounds and monitoring rather than adding randomness blindly.

## Feedback, fairness, and safety

Popularity can concentrate exposure on already popular items. Historical interactions may encode
position bias, unequal catalog access, and previous recommendation policies. Sensitive attributes can
enter through proxies even when omitted.

Inspect exposure and outcomes across relevant groups, creators, categories, and new/long-tail items.
Add explicit filters for unsafe/ineligible content. A model score should never bypass policy rules,
and fairness goals must be defined with affected domain experts rather than inferred from one metric.

## Recommender pitfalls

- Random splits leak future catalog and popularity information.
- Evaluating against items unavailable at prediction time changes the task unfairly.
- Duplicate ranked IDs waste positions and distort metrics.
- Treating every non-click as dislike ignores exposure and position.
- Comparing algorithms with different candidate sets invalidates the comparison.
- Optimizing clicks alone can reward sensational, repetitive, or low-trust content.
- Omitting deterministic ties makes tests and user experience unstable.
- Adding neural embeddings without a baseline hides whether complexity helped.

## Recommendation checklist

- [ ] Event, exposure, positive signal, relevance window, and cutoff are defined.
- [ ] Candidate eligibility and seen-item policy match serving behavior.
- [ ] Popularity/random/product-rule baselines use the same candidates and split.
- [ ] Ranked IDs are unique and tie ordering is deterministic.
- [ ] K and metric denominator behavior are documented.
- [ ] Unknown users/items and short candidate lists have explicit fallbacks.
- [ ] Coverage, diversity, latency, safety, and group/creator slices accompany relevance.
- [ ] Training data and metrics account for the prior system's feedback loop.

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

- Add a brand-new user and define a deterministic fallback.
- Compare Precision@2 when relevant items contain one versus four items.
- Move the temporal cutoff and explain how the candidate set and Recall@2 change.
- Add a duplicate event and decide whether it represents more preference or data duplication.
- Solve [Recommend unseen items](../../exercises/hard/06_recommender/README.md).

## References

- [Google ML recommendation overview](https://developers.google.com/machine-learning/recommendation) —
  free conceptual guide to candidate generation, scoring, and reranking; not a universal standard.
- [Recommender Systems Handbook](https://link.springer.com/book/10.1007/978-1-0716-2197-4) — paid
  edited reference covering algorithms and evaluation; verify chapter/version access separately.
- [MovieLens datasets and terms](https://grouplens.org/datasets/movielens/) — official, free research
  dataset catalog with required usage terms; this course does not download MovieLens.
- [NDCG in scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html) —
  official, free API definition for one implementation of discounted ranking gain.
- [Local metrics guide](../../docs/metrics.md#retrieval-and-recommenders) — course definitions and
  interpretation questions used by the examples.
