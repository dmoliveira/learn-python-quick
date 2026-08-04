from __future__ import annotations

import numpy as np
import pytest

from learn_python_quick.attention import (
    cosine_similarity_matrix,
    scaled_dot_product_attention,
    tfidf_search,
)
from learn_python_quick.evaluation import (
    classification_metrics,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    regression_metrics,
)
from learn_python_quick.recommender import Interaction, recommend_popular_unseen


def test_regression_and_classification_metric_values() -> None:
    regression = regression_metrics([1.0, 2.0, 3.0], [1.0, 2.0, 4.0])
    assert regression["mae"] == pytest.approx(1 / 3)
    assert regression["rmse"] == pytest.approx(np.sqrt(1 / 3))
    classification = classification_metrics(
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        positive_scores=[0.1, 0.6, 0.8, 0.9],
    )
    assert classification["precision"] == pytest.approx(2 / 3)
    assert classification["recall"] == 1.0
    assert classification["roc_auc"] > 0.8


def test_ranking_metrics_define_empty_and_invalid_cases() -> None:
    ranking = ["b", "a", "c"]
    relevant = {"a", "c"}
    assert precision_at_k(ranking, relevant, k=2) == 0.5
    assert recall_at_k(ranking, relevant, k=2) == 0.5
    assert reciprocal_rank(ranking, relevant) == 0.5
    assert 0 < ndcg_at_k(ranking, relevant, k=3) <= 1
    assert recall_at_k([], set(), k=1) == 0
    with pytest.raises(ValueError, match="k"):
        precision_at_k(ranking, relevant, k=0)
    with pytest.raises(ValueError, match="unique"):
        recall_at_k(["a", "a"], {"a"}, k=2)
    with pytest.raises(ValueError, match="unique"):
        ndcg_at_k(["a", "a"], {"a"}, k=2)
    with pytest.raises(ValueError, match="unique"):
        reciprocal_rank(["a", "a"], {"a"})


def test_attention_shapes_weights_and_similarity() -> None:
    tokens = np.eye(3)
    output, weights = scaled_dot_product_attention(tokens, tokens, tokens)
    assert output.shape == (3, 3)
    assert weights.sum(axis=1) == pytest.approx(np.ones(3))
    similarity = cosine_similarity_matrix([[1, 0], [1, 0], [0, 0]])
    assert similarity[0, 1] == 1
    assert similarity[2, 2] == 0
    with pytest.raises(ValueError, match="shapes"):
        scaled_dot_product_attention([[1, 2]], [[1, 2, 3]], [[1]])


def test_tfidf_search_and_popularity_recommendations_are_stable() -> None:
    results = tfidf_search(["python api", "model metrics", "python types"], "python", top_k=2)
    assert [result.index for result in results] == [0, 2]
    rows = [
        Interaction("u1", "a"),
        Interaction("u2", "a"),
        Interaction("u2", "b"),
        Interaction("u3", "b"),
        Interaction("u3", "c"),
    ]
    assert recommend_popular_unseen(rows, user_id="u1", k=2) == ["b", "c"]
