"""Sparse text retrieval and one NumPy attention head."""

import numpy as np

from learn_python_quick.attention import scaled_dot_product_attention, tfidf_search


def main() -> None:
    documents = [
        "debug a Python API timeout",
        "evaluate a classification model",
        "vectorize numerical work with NumPy",
        "serve a model with a typed API",
    ]
    for result in tfidf_search(documents, "Python model API", top_k=2):
        print(f"search score={result.score:.3f} text={result.text!r}")

    tokens = np.array([[1.0, 0.0], [0.5, 0.5], [0.0, 1.0]])
    output, weights = scaled_dot_product_attention(tokens, tokens, tokens)
    print(f"attention row sums={weights.sum(axis=1).round(6)}")
    print(f"output shape={output.shape}")


if __name__ == "__main__":
    main()
