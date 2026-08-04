# 12 · Performance and quality ⚙️

**Time:** 60 minutes · **Prerequisites:** Any completed learning path

## Outcomes

You will be able to:

- measure wall time and identify a bottleneck before optimizing;
- use better algorithms, vectorization, generators, batching, and caching intentionally;
- recognize time/memory/readability trade-offs;
- design tests around behavior and edge cases;
- use formatting, linting, typing, review, and CI as complementary signals.

## Optimize in the right order

1. Define the required behavior and budget.
2. Measure a realistic workload with `timeit`, `cProfile`, or a production trace.
3. Fix unnecessary work or algorithmic complexity first.
4. Use built-ins, NumPy vectorization, batching, or concurrency only where they fit.
5. Measure again and preserve a correctness test.

Common useful techniques:

- use a set for repeated membership tests;
- stream with generators when all items are not needed together;
- batch I/O or model inference to amortize overhead;
- select narrow DataFrame columns and suitable dtypes;
- cache pure, repeated, bounded computations with `lru_cache`;
- use vectorized array operations for numeric loops;
- push network concurrency only after rate limits, timeouts, and backpressure are designed.

Do not vectorize merely to remove every Python loop. Large temporary arrays may increase memory, and
clear code may already meet the budget.

## Quality is layered evidence

| Tool | Catches |
|---|---|
| formatter | irrelevant style differences |
| linter | likely mistakes and maintainability issues |
| type checker | inconsistent contracts before runtime |
| unit/contract tests | known behavioral cases |
| integration smoke | boundaries that compose incorrectly |
| review | unclear design, missing risks, and incorrect assumptions |
| monitoring | behavior that only real traffic reveals |

No layer proves correctness alone. Tests should cover normal, empty, boundary, invalid, and regression
cases. For ML, also test shapes, leakage boundaries, metric ranges, deterministic configuration, and
artifact/API schemas.

## Run it

```bash
uv run python chapters/12_performance_and_quality/example.py
make check
make wheel-smoke
```

The micro-timing is illustrative; compare behavior and order of magnitude, not an exact duration.

## Try it

- Benchmark list versus set membership at several sizes.
- Profile a pandas row loop, then replace it with a vectorized expression.
- Add one regression test before optimizing a function.
- Try [Profile a slow feature step](../../docs/exercise-guide.md#challenge-catalog).

## References

- [`timeit`](https://docs.python.org/3/library/timeit.html) and [`cProfile`](https://docs.python.org/3/library/profile.html)
- [Python performance tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [NumPy performance and broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [pytest documentation](https://docs.pytest.org/)
