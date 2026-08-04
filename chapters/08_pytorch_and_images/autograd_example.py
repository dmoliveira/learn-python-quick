"""Inspect one optional PyTorch gradient and apply one update."""

from typing import Any

from learn_python_quick.optional import require_module


def main() -> None:
    torch: Any = require_module("torch", extra="deep")
    torch.set_num_threads(1)

    inputs = torch.tensor([1.0, 2.0, 3.0])
    targets = torch.tensor([2.0, 4.0, 6.0])
    weight = torch.tensor(1.0, requires_grad=True)

    loss = ((weight * inputs - targets) ** 2).mean()
    loss.backward()
    print(
        f"before weight={weight.item():.3f} loss={loss.item():.3f} gradient={weight.grad.item():.3f}"
    )

    with torch.no_grad():
        weight -= 0.1 * weight.grad
    weight.grad.zero_()
    print(f"after weight={weight.item():.3f} gradient_reset={weight.grad.item():.1f}")


if __name__ == "__main__":
    main()
