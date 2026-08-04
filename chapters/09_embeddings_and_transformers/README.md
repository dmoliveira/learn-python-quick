# 09 · Embeddings and transformers 🔤

**Time:** 75 minutes · **Prerequisites:** [NumPy](../05_numpy_and_pandas/README.md) and basic neural
networks from [Chapter 08](../08_pytorch_and_images/README.md)

## Outcomes

You will be able to:

- explain an embedding as a task-dependent vector representation;
- build a transparent TF-IDF retrieval baseline;
- compare vectors with cosine similarity;
- calculate scaled dot-product attention;
- name the main blocks in a classic transformer encoder.

## Start with a retrieval baseline

TF-IDF represents a document with sparse term weights. It is not a neural embedding, but it is fast,
explainable, and often a strong lexical-search baseline. Evaluate it before adding a large model.

Cosine similarity compares vector direction:

```text
cos(a, b) = (a · b) / (||a|| ||b||)
```

Similarity only has meaning relative to how vectors were created and what task labels say is
relevant. Evaluate text retrieval with Recall@K, MRR, or NDCG on held-out labeled queries.

## Attention, one head

For token matrices `Q`, `K`, and `V`, scaled dot-product attention is:

```text
softmax(Q Kᵀ / √d) V
```

Each query scores keys, softmax turns scores into weights, and those weights mix value vectors.
Scaling by the square root of key width keeps logits from becoming too large.

A classic encoder layer adds multi-head attention, residual connections, layer normalization, a
position-wise feed-forward network, and positional information. Training also needs tokenization,
masks, an objective, extensive data, and optimization. This chapter implements only the small
mathematical core; it does not pretend to train a language model.

## Run it

```bash
uv run python chapters/09_embeddings_and_transformers/example.py
```

The example uses NumPy and scikit-learn only. No model or tokenizer is downloaded.

## Try it

- Add a document that shares words but has a different meaning; inspect TF-IDF's weakness.
- Change one query vector and verify every attention row still sums to 1.
- Add a causal mask on paper before implementing it.
- Try [Build semantic search](../../docs/exercise-guide.md#challenge-catalog).

## References

- [scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [PyTorch transformer building blocks tutorial](https://pytorch.org/tutorials/intermediate/transformer_building_blocks.html)
- [Sentence Transformers evaluation](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html)
