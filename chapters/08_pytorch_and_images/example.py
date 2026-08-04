"""Train a tiny optional PyTorch MLP on packaged digit images."""

from learn_python_quick.deep_learning import train_digits_mlp


def main() -> None:
    run = train_digits_mlp(seed=42, epochs=8, hidden_units=48)
    print(
        f"epochs={run.epochs} loss={run.initial_loss:.3f}->{run.final_loss:.3f} "
        f"test_accuracy={run.accuracy:.3f}"
    )


if __name__ == "__main__":
    main()
