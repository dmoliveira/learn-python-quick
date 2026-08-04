# 09 · Embeddings and transformers 🔤

**Time:** 75 minutes · **Prerequisites:** [NumPy](../05_numpy_and_pandas/README.md) and basic neural
networks from [Chapter 08](../08_pytorch_and_images/README.md)

## Outcomes

You will be able to:

- explain an embedding as a task-dependent vector representation;
- build and evaluate a transparent TF-IDF retrieval baseline;
- compare vectors with cosine similarity;
- calculate scaled dot-product attention and track its shapes;
- name the main blocks in a classic transformer encoder;
- distinguish a mathematical demonstration from a pretrained language system.

## A vector gets meaning from its construction

An **embedding** maps an item—word, document, image, user, or product—to a numeric vector. Nearby
vectors are expected to be similar according to a training objective or feature construction method.
There is no universal semantic coordinate system: distance is useful only for a named task and
evaluated population.

```text
item ── representation function ──> vector ── similarity/ranking ──> decision
```

Ask four questions before using an embedding:

1. Which items and languages were represented during fitting?
2. Which objective made vectors close or far apart?
3. Which similarity function and normalization are used?
4. Which labeled task demonstrates that the ranking is useful?

## Start with a lexical retrieval baseline

TF-IDF represents each document with sparse term weights. **Term frequency** increases weight for
words used in a document; **inverse document frequency** reduces weight for words common across many
documents. It is not a neural embedding, but it is fast, inspectable, offline, and often a strong
lexical-search baseline.

```python
results = tfidf_search(
    ["debug a Python API timeout", "evaluate classifier recall"],
    "Python timeout",
    top_k=2,
)
```

TF-IDF cannot naturally understand that two texts with no shared terms may mean similar things. It can
also rank keyword overlap that has the wrong meaning. Those failures are useful evidence for deciding
whether a learned embedding is worth its cost.

## Cosine similarity compares direction

For nonzero vectors `a` and `b`:

```text
cos(a, b) = (a · b) / (||a|| ||b||)
```

Cosine similarity ranges from -1 to 1 for real vectors, although many text representations produce
nonnegative values. It ignores magnitude and compares direction. Define zero-vector behavior
explicitly because division by zero has no meaningful angle. The course helper returns zeros for
comparisons involving a zero vector.

Similarity is not a calibrated probability. A score of `0.8` has no universal relevance meaning, and
scores from different embedding models may not be comparable.

## Retrieval evaluation needs labels and candidates

A retrieval example needs more than a plausible top result. Define:

- a fixed document/candidate collection;
- held-out queries;
- the relevant document IDs for each query;
- a cutoff `K` that matches the product surface;
- deterministic handling of ties and duplicate IDs.

Useful metrics answer different ranking questions:

| Metric | Question |
|---|---|
| Precision@K | What fraction of the first K results is relevant? |
| Recall@K | What fraction of known relevant items appeared in the first K? |
| Reciprocal rank | How early did the first relevant item appear? |
| NDCG@K | Did highly relevant items appear near the top, with graded/binary gain? |

[`retrieval_evaluation_example.py`](retrieval_evaluation_example.py) evaluates three fixed queries
against four local documents and reports Recall@2 and mean reciprocal rank (MRR):

```bash
uv run python chapters/09_embeddings_and_transformers/retrieval_evaluation_example.py
```

The labels are handcrafted for teaching and are not a reusable benchmark. The example's value is its
evaluation shape: IDs, candidates, relevance judgments, per-query results, and an aggregate.

## Attention mixes information by relevance weights

For token matrices `Q` (queries), `K` (keys), and `V` (values), one scaled dot-product attention head
is:

```text
softmax(Q Kᵀ / √d_key) V
```

Track shapes before values:

| Tensor | Example shape | Meaning |
|---|---|---|
| `Q` | `(query_tokens, key_width)` | what each output position looks for |
| `K` | `(source_tokens, key_width)` | what each source position offers for matching |
| `Q Kᵀ` | `(query_tokens, source_tokens)` | pairwise attention logits |
| weights | `(query_tokens, source_tokens)` | normalized source weights per query |
| `V` | `(source_tokens, value_width)` | information available to mix |
| output | `(query_tokens, value_width)` | weighted value combinations |

Scaling by `√d_key` prevents dot products from growing solely because vectors are wider. Stable
softmax subtracts each row's maximum before exponentiation. Every unmasked weight row should sum to
approximately one.

### Masks change which positions are eligible

A padding mask prevents attention to placeholder tokens. A causal mask prevents a position from
looking at later positions. Apply the mask to logits before softmax, using a value that makes masked
weights effectively zero. Confirm that at least one position remains available per query; a fully
masked row can produce undefined normalization.

Attention weights show how one computation mixed value vectors. They are not automatically faithful
natural-language explanations or causal attributions.

## From one head to a transformer

A classic transformer encoder layer combines:

1. multi-head self-attention;
2. a residual connection and layer normalization;
3. a position-wise feed-forward network;
4. another residual connection and normalization.

Multiple heads learn separate query/key/value projections. Positional information is needed because
self-attention alone does not encode token order. A complete language system also needs tokenization,
an objective, large data, optimization, context limits, decoding behavior, and evaluation.

The original architecture paper is a foundation, not a current production recipe. Modern systems
vary normalization order, position encoding, attention implementation, objectives, and serving
strategy. Check the documentation for the exact model/version being used.

## Worked mathematical example

The original chapter example runs local TF-IDF search and a single NumPy attention head:

```bash
uv run python chapters/09_embeddings_and_transformers/example.py
```

It verifies attention row sums and output shape. It does not download a tokenizer, pretrained model,
or dataset, and it does not claim to train a transformer.

## System trade-offs beyond relevance

Learned embeddings add artifact size, inference cost, batch/latency choices, model versioning, and
index refresh. A retrieval system must keep document vectors, query vectors, and similarity settings
compatible. Changing the embedding model usually requires rebuilding the index.

Evaluate latency, memory, index freshness, unsupported languages, long-text truncation, and privacy in
addition to relevance. Text may contain personal or confidential data; do not send it to an external
embedding service without an explicit data-handling decision.

## Embedding and attention pitfalls

- Treating cosine similarity as probability gives scores unsupported meaning.
- Evaluating on the same queries used to tune prompts/documents overfits the benchmark.
- Letting duplicate documents cross train/test or candidate boundaries inflates retrieval metrics.
- Ignoring stable IDs makes relevance labels impossible to audit.
- Forgetting a padding/causal mask lets attention use invalid positions.
- Computing naive attention for very long sequences can exhaust quadratic memory.
- Downloading a model implicitly breaks offline, licensing, and reproducibility guarantees.
- Reading attention weights as causal explanation overstates what the calculation proves.

## Retrieval and transformer checklist

- [ ] Representation model, version, objective, and supported input are recorded.
- [ ] Candidate collection and relevance labels are versioned.
- [ ] A transparent lexical or popularity baseline is measured first.
- [ ] Similarity, normalization, tie order, duplicate policy, and cutoff K are explicit.
- [ ] Per-query failures and important language/domain slices are inspected.
- [ ] Attention shapes and mask semantics are tested on small arrays.
- [ ] Index refresh, latency, memory, privacy, and licensing are considered.
- [ ] No hidden model or data download occurs in the default path.

## Run it

```bash
uv run python chapters/09_embeddings_and_transformers/example.py
uv run python chapters/09_embeddings_and_transformers/retrieval_evaluation_example.py
```

Both examples use NumPy and scikit-learn only. No model or tokenizer is downloaded.

## Try it

- Add a document that shares words but has a different meaning; inspect TF-IDF's weakness.
- Add one query with two relevant documents and compare Precision@2 with Recall@2.
- Change one query vector and verify every attention row still sums to 1.
- Draw a causal mask for four tokens before implementing it.
- Try [Build semantic search](../../docs/exercise-guide.md#challenge-catalog).

## References

- [scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) —
  official, free TF-IDF and sparse text-feature guide.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — free primary paper for the original
  transformer architecture; later systems differ in important details.
- [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) — free educational
  implementation that connects equations with code; check its stated framework version.
- [PyTorch transformer building blocks](https://pytorch.org/tutorials/intermediate/transformer_building_blocks.html) —
  official, free tutorial for current PyTorch attention components and performance considerations.
- [Sentence Transformers evaluation](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html) —
  official, free evaluator catalog for a popular optional ecosystem; not required by this course.
