from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone

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
from learn_python_quick.recommender import (
    Interaction,
    recommend_popular_unseen,
    temporal_user_split,
)


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


@pytest.mark.parametrize(
    ("y_true", "y_pred", "message"),
    [
        ([], [], "empty"),
        ([0, 1], [0], "equal"),
    ],
)
def test_prediction_metrics_validate_pair_shapes(
    y_true: list[object],
    y_pred: list[object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        regression_metrics(y_true, y_pred)
    with pytest.raises(ValueError, match=message):
        classification_metrics(y_true, y_pred)


def test_regression_metrics_support_matching_multioutput_targets() -> None:
    result = regression_metrics(
        [[1.0, 10.0], [2.0, 20.0]],
        [[1.0, 12.0], [3.0, 20.0]],
    )
    assert result["mae"] == pytest.approx(0.75)
    with pytest.raises(ValueError, match="equal shape"):
        regression_metrics([[1.0, 2.0]], [[1.0], [2.0]])
    with pytest.raises(ValueError, match="one- or two-dimensional"):
        regression_metrics([[[1.0]]], [[[1.0]]])


def test_classification_metrics_reject_multidimensional_labels() -> None:
    with pytest.raises(ValueError, match="one-dimensional"):
        classification_metrics([[0, 1]], [[0, 1]])


def test_classification_metrics_validate_labels_and_scores() -> None:
    with pytest.raises(ValueError, match="0 or 1"):
        classification_metrics([0, 2], [0, 1])
    with pytest.raises(ValueError, match="one-dimensional"):
        classification_metrics([0, 1], [0, 1], positive_scores=[[0.1, 0.9]])
    with pytest.raises(ValueError, match="match y_true"):
        classification_metrics([0, 1], [0, 1], positive_scores=[0.1])
    with pytest.raises(ValueError, match="finite numbers"):
        classification_metrics([0, 1], [0, 1], positive_scores=[0.1, np.nan])
    with pytest.raises(ValueError, match="finite numbers"):
        classification_metrics([0, 1], [0, 1], positive_scores=["low", "high"])
    with pytest.raises(ValueError, match="both classes"):
        classification_metrics([1, 1], [1, 1], positive_scores=[0.2, 0.8])

    result = classification_metrics(
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        positive_scores=[-4.0, -2.0, 2.0, 5.0],
    )
    assert result["roc_auc"] == 1.0


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
    with pytest.raises(ValueError, match="at least one"):
        cosine_similarity_matrix(np.empty((0, 2)))
    with pytest.raises(ValueError, match="non-empty"):
        scaled_dot_product_attention(np.empty((0, 2)), [[1, 2]], [[1]])


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


def test_tfidf_search_defines_empty_text_boundaries() -> None:
    assert tfidf_search([], "python") == []
    with pytest.raises(ValueError, match="query"):
        tfidf_search(["python"], " ")
    with pytest.raises(ValueError, match="query"):
        tfidf_search(["python"], "the and")
    with pytest.raises(ValueError, match="documents"):
        tfidf_search(["", "the and"], "python")
    results = tfidf_search(["", "python types"], "python", top_k=2)
    assert [result.index for result in results] == [1, 0]


def test_temporal_user_split_preserves_time_and_unseen_contract() -> None:
    cutoff = datetime(2026, 7, 10, tzinfo=UTC)
    rows = [
        Interaction("u1", "seen", 1, datetime(2026, 7, 1, tzinfo=UTC)),
        Interaction("u2", "future", 1, datetime(2026, 7, 2, tzinfo=UTC)),
        Interaction("u2", "not-candidate", 0, datetime(2026, 7, 3, tzinfo=UTC)),
        Interaction("u1", "seen", 1, datetime(2026, 7, 10, tzinfo=UTC)),
        Interaction("u1", "boundary", 1, cutoff),
        Interaction("u1", "ignored", 0, datetime(2026, 7, 11, tzinfo=UTC)),
        Interaction("u1", "future", 1, datetime(2026, 7, 12, tzinfo=UTC)),
        Interaction("u1", "not-candidate", 1, datetime(2026, 7, 13, tzinfo=UTC)),
    ]
    training, relevant = temporal_user_split(rows, cutoff=cutoff, user_id="u1")
    assert training == rows[:3]
    assert relevant == {"future"}


def test_temporal_user_split_requires_utc_timestamps() -> None:
    aware = datetime(2026, 7, 1, tzinfo=UTC)
    with pytest.raises(ValueError, match="cutoff"):
        temporal_user_split([], cutoff=datetime(2026, 7, 10), user_id="u1")
    with pytest.raises(ValueError, match="occurred_at"):
        temporal_user_split([Interaction("u1", "a")], cutoff=aware, user_id="u1")
    with pytest.raises(ValueError, match="timezone-aware"):
        temporal_user_split(
            [Interaction("u1", "a", 1, datetime(2026, 7, 1))],
            cutoff=aware,
            user_id="u1",
        )
    plus_one = timezone(timedelta(hours=1))
    with pytest.raises(ValueError, match="UTC"):
        temporal_user_split(
            [Interaction("u1", "a", 1, datetime(2026, 7, 1, tzinfo=plus_one))],
            cutoff=aware,
            user_id="u1",
        )
