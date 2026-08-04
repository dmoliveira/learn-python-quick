"""Optional, tiny PyTorch training examples designed for a CPU."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

from learn_python_quick.optional import require_module
from learn_python_quick.recommender import Interaction


@dataclass(frozen=True, slots=True)
class DeepTrainingRun:
    accuracy: float
    initial_loss: float
    final_loss: float
    epochs: int


def seed_everything(seed: int) -> None:
    """Set common seeds; cross-platform bitwise equality is not promised."""
    random.seed(seed)
    np.random.seed(seed)
    torch: Any = require_module("torch", extra="deep")
    torch.manual_seed(seed)


def train_digits_mlp(
    *,
    seed: int = 42,
    epochs: int = 8,
    hidden_units: int = 48,
) -> DeepTrainingRun:
    """Train a two-layer MLP on packaged 8-by-8 digit images."""
    if epochs < 1 or hidden_units < 1:
        raise ValueError("epochs and hidden_units must be positive")
    torch: Any = require_module("torch", extra="deep")
    seed_everything(seed)
    torch.set_num_threads(1)

    digits = load_digits()
    features = digits.data.astype("float32") / 16.0
    targets = digits.target.astype("int64")
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        targets,
        test_size=0.2,
        random_state=seed,
        stratify=targets,
    )
    train_x = torch.tensor(x_train, dtype=torch.float32)
    train_y = torch.tensor(y_train, dtype=torch.long)
    test_x = torch.tensor(x_test, dtype=torch.float32)
    test_y = torch.tensor(y_test, dtype=torch.long)

    model = torch.nn.Sequential(
        torch.nn.Linear(64, hidden_units),
        torch.nn.ReLU(),
        torch.nn.Linear(hidden_units, 10),
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
    loss_function = torch.nn.CrossEntropyLoss()
    losses: list[float] = []

    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        logits = model(train_x)
        loss = loss_function(logits, train_y)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().item()))

    model.eval()
    with torch.no_grad():
        predicted = model(test_x).argmax(dim=1)
        accuracy = float((predicted == test_y).float().mean().item())
    return DeepTrainingRun(accuracy, losses[0], losses[-1], epochs)


def train_neural_recommender(
    interactions: list[Interaction],
    *,
    user_id: str,
    k: int = 3,
    seed: int = 42,
    epochs: int = 30,
) -> list[str]:
    """Fit tiny user/item embeddings and rank unseen items for one user."""
    if k < 1 or epochs < 1:
        raise ValueError("k and epochs must be positive")
    torch: Any = require_module("torch", extra="deep")
    seed_everything(seed)
    torch.set_num_threads(1)

    users = sorted({row.user_id for row in interactions})
    items = sorted({row.item_id for row in interactions})
    if user_id not in users:
        raise ValueError(f"unknown user: {user_id}")
    user_index = {user: index for index, user in enumerate(users)}
    item_index = {item: index for index, item in enumerate(items)}
    positive = {(row.user_id, row.item_id) for row in interactions if row.rating > 0}

    pairs = [(user, item) for user in users for item in items]
    user_ids = torch.tensor([user_index[user] for user, _ in pairs], dtype=torch.long)
    item_ids = torch.tensor([item_index[item] for _, item in pairs], dtype=torch.long)
    labels = torch.tensor(
        [float((user, item) in positive) for user, item in pairs],
        dtype=torch.float32,
    )

    user_embeddings = torch.nn.Parameter(torch.randn(len(users), 8) * 0.1)
    item_embeddings = torch.nn.Parameter(torch.randn(len(items), 8) * 0.1)
    optimizer = torch.optim.Adam([user_embeddings, item_embeddings], lr=0.08)
    loss_function = torch.nn.BCEWithLogitsLoss()
    for _ in range(epochs):
        optimizer.zero_grad()
        logits = (user_embeddings[user_ids] * item_embeddings[item_ids]).sum(dim=1)
        loss = loss_function(logits, labels)
        loss.backward()
        optimizer.step()

    seen = {item for user, item in positive if user == user_id}
    candidates = [item for item in items if item not in seen]
    with torch.no_grad():
        user_vector = user_embeddings[user_index[user_id]]
        scored = [
            (float((user_vector * item_embeddings[item_index[item]]).sum().item()), item)
            for item in candidates
        ]
    return [item for _, item in sorted(scored, key=lambda pair: (-pair[0], pair[1]))[:k]]
