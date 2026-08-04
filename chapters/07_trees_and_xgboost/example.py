"""Compare small decision-tree and random-forest baselines."""

from learn_python_quick.ml import compare_tree_models


def main() -> None:
    for model, accuracy in compare_tree_models(seed=42).items():
        print(f"{model}: accuracy={accuracy:.3f}")


if __name__ == "__main__":
    main()
