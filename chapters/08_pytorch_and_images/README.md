# 08 · PyTorch and image models 🔥

**Time:** 75 minutes · **Prerequisites:** [ML workflows](../06_ml_workflows_and_metrics/README.md) ·
**Extra:** `uv sync --dev --extra deep`

## Outcomes

You will be able to:

- create tensors and understand shape, dtype, device, and gradients;
- define an MLP from linear layers and nonlinear activations;
- write the train → loss → backward → update loop;
- switch correctly between training, evaluation, and no-gradient modes;
- evaluate a small image classifier beyond its training loss.

## The training loop

PyTorch tensors are arrays that can record operations for automatic differentiation. A minimal
supervised loop is:

```python
model.train()
for features, labels in batches:
    optimizer.zero_grad()
    logits = model(features)
    loss = loss_function(logits, labels)
    loss.backward()
    optimizer.step()
```

The model returns **logits**. `CrossEntropyLoss` combines log-softmax and negative log likelihood, so
do not apply softmax before that loss. During evaluation, call `model.eval()` and use
`torch.no_grad()`.

## Image example

The packaged Digits dataset has 1,797 grayscale images, each only 8 by 8 pixels. The example flattens
each image to 64 values, scales pixels to 0–1, and trains a `64 → 48 → 10` MLP for eight full-batch
epochs on one CPU thread. It is intentionally small and should not be treated as a modern vision
architecture.

For larger images, convolutional networks or vision transformers preserve more structure. Always
check per-class errors and inspect incorrect images. Image labels and data collection can encode
social and sampling bias.

Seeds improve repeatability but do not guarantee bitwise equality across PyTorch versions, devices,
or platforms.

## Run it

```bash
uv sync --dev --extra deep
uv run python chapters/08_pytorch_and_images/example.py
```

Expected accuracy is comfortably above a 10% random baseline; tests use a broad lower bound rather
than an exact float.

## Try it

- Compare no hidden layer with 16 and 48 hidden units.
- Plot a confusion matrix and inspect the most confused digit pair.
- Add mini-batches, then measure whether they help this tiny dataset.
- Try [Improve the digits MLP](../../docs/exercise-guide.md#challenge-catalog).

## References

- [PyTorch tensors](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
- [Build a neural network](https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
- [Optimization loop](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [scikit-learn Digits dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset)
