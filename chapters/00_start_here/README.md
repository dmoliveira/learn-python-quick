# 00 · Start here 🚦

**Time:** 15 minutes · **Prerequisites:** Git and uv

## Outcomes

You will be able to:

- run code inside the locked project environment;
- find chapters, exercises, solutions, datasets, and reusable code;
- use the course loop: read → run → change → test → explain;
- tell the difference between repository tests and learner exercise tests.

## The smallest useful loop

Do not read every chapter before coding. Run one example, predict what a change will do, make that
change, and rerun it. A short feedback loop teaches more than copying a large notebook.

```text
chapter README       explains why
chapter example.py   shows one working path
exercise answer.py   is your implementation space
public test           states observable behavior
solution              explains one possible answer
```

The reusable functions live in `src/learn_python_quick/`. Scripts import the installed package, so
they behave like real application code rather than relying on a special working directory.

## Build the learning habit

A useful study session is an experiment, not a reading marathon:

1. **Predict** one observable result before running code.
2. **Run** the smallest command that can test the prediction.
3. **Change** one input or rule—not five things together.
4. **Test** normal, empty, boundary, and invalid input.
5. **Explain** why the result changed in your own words.

Prediction matters because it exposes your current mental model. If the output surprises you, you
have found something worth learning. An assertion turns the prediction into executable evidence:

```python
summary = summarize_sales(rows)
assert summary.revenue == 11.0
```

Do not delete a surprising assertion immediately. First inspect the input, function contract, and
actual value. Then decide whether the code or the prediction was wrong.

## Pick the right command

| Question | Command | Expected result |
|---|---|---|
| Is the repository healthy? | `make check` | Green |
| Is my learner answer complete? | `make exercise ID=...` | Fails until solved |
| Do I need the full traceback? | `make exercise-verbose ID=...` | Detailed learner failure |
| Does packaged code install cleanly? | `make wheel-smoke` | Green |
| Did an optional integration change? | `make setup-all && make test-optional` | Green |

An expected learner failure is not a broken repository. The concise exercise runner names the file
and function to edit without revealing the algorithm.

## A first debugging decision tree

- **Import error:** confirm `uv sync --dev` completed and run through `uv run`.
- **Assertion failure:** print or inspect expected versus actual values and reduce the input.
- **Validation error:** read the field/location and compare it with the public contract.
- **Unexpected network attempt:** stop; default examples must use local data or a fake transport.
- **Slow model/example:** check dataset size, epochs, threads, and whether the optional path is active.

## Worked learning loop

[`learning_loop_example.py`](learning_loop_example.py) predicts revenue, proves it with an assertion,
then triggers one documented boundary error. Notice that the exception is narrow and expected; an
unrelated exception would still stop the script.

```bash
uv run python chapters/00_start_here/learning_loop_example.py
```

Try changing only `units`. Write the expected revenue first, then update the assertion. This small
discipline scales to feature pipelines, model metrics, and API responses.

## Setup completion checklist

- [ ] `uv run python --version` reports a supported interpreter.
- [ ] `uv run lpq roadmap` points to Chapter 00 and the progress checklist.
- [ ] `make check` is green.
- [ ] You can explain why an untouched exercise fails.
- [ ] You changed one value in an example and predicted the result correctly.

## Run it

From the repository root:

```bash
uv sync --dev
uv run python chapters/00_start_here/example.py
uv run python chapters/00_start_here/learning_loop_example.py
make check
```

Expected example output includes the package version and `best seller: tea`.

## Try it

1. Change one input row in [`example.py`](example.py) and predict the new best seller.
2. Run `uv run lpq roadmap`.
3. Open the [fast review path](../../docs/learning-paths.md#-fast-python-review-34-hours).
4. Continue to [Python fundamentals](../01_python_fundamentals/README.md).

## References

- [uv: working on projects](https://docs.astral.sh/uv/guides/projects/)
- [Python tutorial](https://docs.python.org/3/tutorial/)
- [The Debugging Book](https://www.debuggingbook.org/) — free, deeper material on systematic
  experiments and failure reduction; use it after the first few chapters.
