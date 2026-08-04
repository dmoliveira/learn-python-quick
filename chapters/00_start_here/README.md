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

## Run it

From the repository root:

```bash
uv sync --dev
uv run python chapters/00_start_here/example.py
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
