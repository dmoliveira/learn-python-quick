# 08 · PyTorch and image models 🔥

**Time:** 75 minutes · **Prerequisites:** [ML workflows](../06_ml_workflows_and_metrics/README.md) ·
**Extra:** `uv sync --dev --extra deep`

## Outcomes

You will be able to:

- create tensors and reason about shape, dtype, device, and gradients;
- inspect a small automatic-differentiation graph;
- define an MLP from linear layers and nonlinear activations;
- write the train → loss → backward → update loop;
- switch correctly between training, evaluation, and no-gradient modes;
- evaluate a small image classifier beyond its training loss.

## A tensor has four important properties

A PyTorch tensor is a multidimensional array. Before investigating values, inspect:

| Property | Question |
|---|---|
| shape | What does each axis represent? |
| dtype | Are these floating features, integer class IDs, or booleans? |
| device | Is storage and computation on CPU, GPU, or another accelerator? |
| `requires_grad` | Should PyTorch record operations to calculate gradients? |

For image classification, a batch is commonly shaped `(batch, channels, height, width)`. The course
Digits data starts as flattened `(rows, 64)` features because each grayscale image is only 8 by 8.
Shape compatibility is not enough: swapping batch and feature axes can still create the wrong model.

```python
features = torch.tensor([[0.0, 1.0], [1.0, 0.0]], dtype=torch.float32)
labels = torch.tensor([0, 1], dtype=torch.long)
```

Classification features are usually floating point, while class IDs passed to `CrossEntropyLoss`
must be integer `long` values. Tensors in one operation normally need compatible devices and dtypes.

## Automatic differentiation records operations

**Automatic differentiation**, often shortened to autograd, applies the chain rule through recorded
tensor operations. A parameter with `requires_grad=True` becomes a leaf in that computation graph:

```python
weight = torch.tensor(1.0, requires_grad=True)
prediction = weight * inputs
loss = ((prediction - targets) ** 2).mean()
loss.backward()
print(weight.grad)
```

`backward()` stores the derivative of loss with respect to `weight` in `weight.grad`. Gradients
accumulate by default, so a training loop must clear them before the next backward pass. Parameter
updates should happen without recording another gradient graph.

[`autograd_example.py`](autograd_example.py) performs one scalar-weight update and then resets the
gradient:

```bash
uv sync --dev --extra deep
uv run python chapters/08_pytorch_and_images/autograd_example.py
```

The example uses fixed tensors, one CPU thread, and no dataset. It is a view of the mechanics, not an
optimizer suitable for a real model.

## Modules turn parameters into a model

`torch.nn.Module` groups parameter tensors and a forward calculation. A small multilayer perceptron
(MLP) can be composed without writing a custom class:

```python
model = torch.nn.Sequential(
    torch.nn.Linear(64, 48),
    torch.nn.ReLU(),
    torch.nn.Linear(48, 10),
)
```

The final layer returns ten **logits**: unconstrained scores, one per class. `CrossEntropyLoss`
combines log-softmax with negative log likelihood. Do not apply softmax before this loss. Apply
softmax only when probabilities are needed for evaluation or a downstream decision.

The hidden width controls capacity but is not a promise that every hidden unit learns a human concept.
An MLP also discards the 2D neighborhood structure when an image is flattened. Convolutional networks
and vision transformers preserve or reconstruct more spatial structure for larger image tasks.

## The training loop, one step at a time

```python
model.train()
for features, labels in batches:
    optimizer.zero_grad()
    logits = model(features)
    loss = loss_function(logits, labels)
    loss.backward()
    optimizer.step()
```

Each line has a separate job:

1. `train()` enables training behavior such as dropout and batch-normalization updates.
2. `zero_grad()` clears gradients left from the previous update.
3. The forward call creates logits and an autograd graph.
4. The loss compares logits with target class IDs.
5. `backward()` calculates parameter gradients.
6. `step()` updates parameters according to the optimizer.

Track more than training loss. A falling loss can coexist with overfitting, label leakage, or weak
minority-class behavior. Use validation data for architecture, epoch, and threshold choices; keep test
data untouched until those choices are fixed.

## Mini-batches are a data contract

A mini-batch must keep each feature row aligned with its label. Shuffling should be reproducible when
debugging, and the final short batch needs an explicit keep/drop policy. Before the loop, validate:

- feature array is 2D and labels are 1D;
- row counts match;
- feature values are finite and have a suitable floating dtype;
- label IDs use an integer dtype and supported range;
- every row appears exactly once per epoch unless sampling says otherwise.

PyTorch `DataLoader` handles common batching, shuffling, worker, and collation behavior. Understand the
array contract before adding parallel workers. The core-only
[tensor batching exercise](../../exercises/hard/11_tensor_batches/README.md) practices alignment and
deterministic shuffling without requiring PyTorch.

## Evaluation changes state and graph behavior

Use both model evaluation mode and disabled gradient recording:

```python
model.eval()
with torch.no_grad():
    logits = model(validation_features)
    predictions = logits.argmax(dim=1)
```

`eval()` changes layers such as dropout and batch normalization. `no_grad()` avoids building the
autograd graph, reducing memory and work. They solve different problems, so one does not replace the
other. Return to `train()` before the next training epoch.

For classification, inspect a confusion matrix, per-class recall, and representative mistakes.
Accuracy alone can hide a class with few examples. For images, examine the actual pixels and label
quality rather than treating every error as an optimization problem.

## Worked problem: tiny digit classifier

The packaged Digits dataset has 1,797 grayscale images, each 8 by 8 pixels. The example flattens each
image to 64 values, scales pixels from 0–16 into 0–1, and trains a `64 → 48 → 10` MLP for eight
full-batch epochs on one CPU thread.

```bash
uv sync --dev --extra deep
uv run python chapters/08_pytorch_and_images/example.py
```

It is intentionally small and is not a modern vision architecture or production benchmark. The data
ships with scikit-learn, requires no network, and has provenance and terms in the
[dataset manifest](../../datasets/manifest.json).

## Repeatability has limits

Set Python, NumPy, and PyTorch seeds and record data order, package versions, device, dtype, and thread
settings. Seeds improve repeatability but do not guarantee bitwise equality across PyTorch versions,
devices, operating systems, or parallel kernels. Compare sensible tolerances and outcome ranges, not
one exact floating-point trace.

## Deep-learning pitfalls

- Applying softmax before `CrossEntropyLoss` changes the intended loss calculation.
- Forgetting `zero_grad()` unintentionally accumulates gradients across updates.
- Evaluating in training mode makes dropout/batch normalization behave differently.
- Tuning on the test set makes the final metric optimistic.
- Calling `.item()` inside every accelerator step can force synchronization and slow training.
- Moving data/model to different devices causes runtime errors or hidden transfers.
- Assuming a seed guarantees identical results across hardware overstates reproducibility.
- Improving aggregate accuracy without class/error review can concentrate failures.

## Training checklist

- [ ] Every tensor axis, dtype, and device has documented meaning.
- [ ] Feature rows and labels remain aligned through shuffle and batching.
- [ ] Logits, loss input, and target shape/dtype match.
- [ ] Gradients are cleared, calculated, and updated in that order.
- [ ] Validation and test data have separate roles.
- [ ] Evaluation uses `eval()` and disabled gradient recording.
- [ ] Metrics include class/error inspection, not training loss alone.
- [ ] Seeds, versions, device, threads, and data split are recorded.

## Run it

```bash
uv sync --dev --extra deep
uv run python chapters/08_pytorch_and_images/autograd_example.py
uv run python chapters/08_pytorch_and_images/example.py
```

## Try it

- Predict the sign of the scalar gradient before running the autograd example.
- Compare no hidden layer with 16 and 48 hidden units on the same split.
- Calculate a confusion matrix and inspect the most confused digit pair.
- Add mini-batches, then measure whether they help this tiny dataset.
- Solve [Prepare tensor batches](../../exercises/hard/11_tensor_batches/README.md).
- Try [Improve the digits MLP](../../docs/exercise-guide.md#challenge-catalog).

## References

- [PyTorch tensors](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) — official,
  free introduction to shape, dtype, device, indexing, and NumPy conversion.
- [PyTorch autograd](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — official,
  free explanation of computation graphs, gradients, and disabled tracking.
- [Build a neural network](https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) —
  official, free `nn.Module`, layer, and model-structure tutorial.
- [Optimization loop](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) —
  official, free training/evaluation loop reference.
- [scikit-learn Digits dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset) —
  official, free source description for the packaged teaching data.
