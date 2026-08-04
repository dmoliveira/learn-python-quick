"""Small embedding-search and attention building blocks."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True, slots=True)
class SearchResult:
    index: int
    text: str
    score: float


def cosine_similarity_matrix(vectors: ArrayLike) -> NDArray[np.float64]:
    """Return pairwise cosine similarity, safely handling zero vectors."""
    matrix = np.asarray(vectors, dtype=np.float64)
    if matrix.ndim != 2:
        raise ValueError("vectors must be a 2D matrix")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    normalized = np.divide(matrix, norms, out=np.zeros_like(matrix), where=norms != 0)
    similarities: NDArray[np.float64] = normalized @ normalized.T
    return similarities


def scaled_dot_product_attention(
    query: ArrayLike,
    key: ArrayLike,
    value: ArrayLike,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Compute one attention head for 2D token matrices using stable softmax."""
    q = np.asarray(query, dtype=np.float64)
    k = np.asarray(key, dtype=np.float64)
    v = np.asarray(value, dtype=np.float64)
    if q.ndim != 2 or k.ndim != 2 or v.ndim != 2:
        raise ValueError("query, key, and value must be 2D")
    if q.shape[1] != k.shape[1] or k.shape[0] != v.shape[0]:
        raise ValueError("attention shapes are incompatible")

    logits = q @ k.T / math.sqrt(k.shape[1])
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(shifted)
    weights = exp_logits / exp_logits.sum(axis=1, keepdims=True)
    return weights @ v, weights


def tfidf_search(documents: list[str], query: str, *, top_k: int = 3) -> list[SearchResult]:
    """Build a transparent sparse-text baseline before neural embeddings."""
    if not documents:
        return []
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([*documents, query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    order = np.argsort(-scores, kind="stable")[:top_k]
    return [SearchResult(int(index), documents[index], float(scores[index])) for index in order]
