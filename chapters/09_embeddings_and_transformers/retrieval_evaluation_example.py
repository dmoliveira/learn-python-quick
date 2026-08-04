"""Evaluate a transparent lexical retrieval baseline on labeled queries."""

from statistics import fmean

from learn_python_quick.attention import tfidf_search
from learn_python_quick.evaluation import recall_at_k, reciprocal_rank


def main() -> None:
    document_ids = ["api-timeout", "model-metrics", "numpy-speed", "typed-serving"]
    documents = [
        "debug timeout retries in a Python API",
        "evaluate classification precision and recall",
        "vectorize numerical arrays with NumPy",
        "serve model predictions with typed request validation",
    ]
    labeled_queries = [
        ("Python API timeout", {"api-timeout"}),
        ("classification recall metric", {"model-metrics"}),
        ("typed model prediction request", {"typed-serving"}),
    ]

    recalls: list[float] = []
    reciprocal_ranks: list[float] = []
    for query, relevant in labeled_queries:
        results = tfidf_search(documents, query, top_k=2)
        ranked_ids = [document_ids[result.index] for result in results]
        recall = recall_at_k(ranked_ids, relevant, k=2)
        rank = reciprocal_rank(ranked_ids, relevant)
        recalls.append(recall)
        reciprocal_ranks.append(rank)
        print(f"query={query!r} results={ranked_ids} recall@2={recall:.2f} rr={rank:.2f}")

    print(f"mean recall@2={fmean(recalls):.2f} mrr={fmean(reciprocal_ranks):.2f}")


if __name__ == "__main__":
    main()
