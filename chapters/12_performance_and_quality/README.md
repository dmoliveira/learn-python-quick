# 12 · Performance and quality ⚙️

**Time:** 60 minutes · **Prerequisites:** Any completed learning path

## Outcomes

You will be able to:

- turn a vague speed concern into a measured behavior and budget;
- identify a bottleneck before optimizing;
- use better algorithms, vectorization, generators, batching, and caching intentionally;
- recognize time, memory, latency, readability, and freshness trade-offs;
- design tests around contracts, edge cases, and regressions;
- use formatting, linting, typing, review, CI, and monitoring as complementary evidence.

## Performance begins with a budget

“Make it faster” is incomplete. Define workload, environment, and required outcome:

```text
For 100,000 feature rows on one CI CPU,
finish under 2 seconds with peak memory under 300 MB,
while matching the reference output within tolerance.
```

An API may care about p95 latency and requests per second. A batch job may care about total runtime,
memory, cloud cost, and completion deadline. Training may care about time to a fixed validation metric,
not simply steps per second. Optimize the constraint that changes the decision.

## Optimize in the right order

1. Define required behavior and a budget.
2. Make a representative workload and correctness oracle.
3. Measure with `timeit`, a profiler, or production trace.
4. Identify the dominant algorithm, I/O, allocation, or wait.
5. Remove unnecessary work or improve complexity first.
6. Apply vectorization, batching, caching, or concurrency only where they fit.
7. Measure again and keep a regression test/benchmark.

A microbenchmark cannot represent network queues, cold starts, data skew, or shared production
resources. A production trace may include noise and unknown causes. Use the smallest measurement that
still answers the real question.

## Algorithm choice can dominate syntax

Repeated membership in a list is linear in the list length; membership in a set is usually constant
average time after building the set. If many lookups reuse the same candidates, paying once to build a
set can change total complexity.

```python
candidate_set = set(candidate_list)
matches = sum(value in candidate_set for value in values)
```

Account for construction and memory. A one-off lookup may not justify a set. Stable output ordering
may still need a list or sorted result because sets do not define the product's ranking.

[`membership_benchmark_example.py`](membership_benchmark_example.py) checks both implementations
return the same count, repeats each timing, and reports medians without asserting a speed ratio:

```bash
uv run python chapters/12_performance_and_quality/membership_benchmark_example.py
```

Timings vary by machine and load. The useful result is the method: same work, correctness first,
multiple observations, and no fragile exact-duration test.

## Vectorization trades Python overhead for array work

NumPy executes many numeric operations in compiled loops. Vectorization can improve clarity and speed
when the data naturally forms dense arrays:

```python
normalized = (values - values.mean()) / values.std()
```

But chained operations may allocate several full-size temporary arrays. Broadcasting can accidentally
create a huge `(rows, rows)` intermediate. Measure peak memory as well as time, and use chunking or
in-place operations only when their mutation contract is safe.

The original chapter example compares readable Python and NumPy z-score implementations and verifies
their outputs with a tolerance:

```bash
uv run python chapters/12_performance_and_quality/example.py
```

Do not vectorize merely to remove every Python loop. Parsing, branching, and small control-flow tasks
may be clearer and fast enough as plain Python.

## Streaming and batching solve different problems

A generator streams values so the whole input need not exist in memory. Batching groups several
values to amortize fixed cost such as a database call, model launch, or request overhead.

```text
streaming: one/few records live at once → lower memory, errors arrive during iteration
batching:  N records per operation       → better throughput, more per-batch memory/latency
```

Choose batch size from measurement and service limits. Larger batches can improve throughput while
worsening single-item latency and memory. Keep a final short batch unless the algorithm explicitly
requires fixed shapes. Preserve row IDs/order so outputs can be correlated.

The [tensor batching exercise](../../exercises/hard/11_tensor_batches/README.md) practices aligned,
deterministic batches and fresh-array ownership.

## Cache only stable, bounded work

Caching trades memory and freshness for avoided computation. `lru_cache` works well for pure functions
with hashable arguments and a bounded key space:

```python
@lru_cache(maxsize=128)
def compute(key: str) -> Result: ...
```

Before caching, decide key completeness, maximum size, invalidation, concurrency, and whether failures
should be cached. Never include secrets in observable cache keys. In ML, model/data version is usually
part of a correct feature or prediction cache key.

The course's recursive Fibonacci function demonstrates memoization, but an iterative algorithm is
still the better design for large inputs. Caching a poor algorithm can hide rather than remove a
complexity problem.

## Concurrency is for independent waiting or work

Concurrency may overlap network/disk waits or distribute CPU work, but it adds scheduling, ordering,
cancellation, retries, and resource pressure. Python threads can help I/O; processes can run Python
CPU work in parallel at serialization/memory cost; numerical libraries may already use native
threads; async coordinates nonblocking I/O rather than making CPU inference free.

Bound concurrency and add backpressure. More workers can reduce throughput when they contend for CPU,
memory bandwidth, database connections, or rate limits. Record thread/process/library settings with
benchmarks.

## Measure with a reproducible protocol

For a useful benchmark:

- verify candidate and reference outputs before timing;
- isolate setup from the operation when appropriate;
- warm up imports/JIT/caches when measuring steady state, or include them when measuring cold start;
- repeat and report a distribution or robust statistic;
- pin workload, data version, Python/package versions, hardware, and thread settings;
- measure memory/allocation when optimization may create large temporaries;
- avoid running unrelated heavy work on the same machine;
- do not assert that one implementation is always a fixed ratio faster.

`timeit` reduces common timing mistakes for small snippets. `cProfile` shows call-level cumulative
time. Sampling profilers and production traces can reveal behavior under realistic load. Profile data
must be interpreted; the hottest function may be necessary work, while its caller chose a wasteful
algorithm.

## Quality is layered evidence

| Layer | Catches | Does not prove |
|---|---|---|
| formatter | irrelevant style differences | behavior |
| linter | likely mistakes and maintainability issues | runtime correctness |
| type checker | inconsistent static contracts | valid external data |
| unit/contract tests | named behavioral cases | every possible input |
| integration smoke | boundaries that compose incorrectly | production reliability |
| review | unclear design, risks, assumptions | absence of all defects |
| CI matrix | repeatability across listed environments | environments not tested |
| monitoring | behavior visible in real traffic | causal explanation |

No layer replaces another. Fast feedback belongs early; expensive realistic checks belong at risk
gates. A green test suite is evidence tied to the cases and environments it ran.

## Test the public contract

Start with behavior that users can observe:

1. normal representative case;
2. empty case when meaningful;
3. minimum/maximum boundary;
4. invalid type/shape/range;
5. deterministic order and tie behavior;
6. input mutation/ownership;
7. a regression case for a prior defect.

Avoid asserting private helper call order unless it is part of the contract. Keep tests deterministic,
offline, and small by default. Inject clocks, random generators, files, and HTTP transports rather
than depending on global live state.

For floating point, use an explained tolerance. For DataFrames/arrays, assert shape, columns/dtype
where contractual, values, and input preservation. For ML, test leakage boundaries, schema, metric
ranges, fixed split/seed configuration, and error handling—not a fragile exact fitted coefficient.

The [prediction envelope exercise](../../exercises/hard/12_prediction_envelope/README.md) demonstrates
strict boundary cases and deterministic serialized output.

## Review for maintainability and operation

Review asks questions tools cannot fully answer:

- Is this the smallest clear design that meets the budget?
- Are boundary, mutation, error, and optional-dependency contracts visible?
- Could data from the future or wrong user cross an ML split?
- Are security/privacy/licensing assumptions documented?
- Can the behavior be observed, rolled back, and owned in production?
- Do comments explain decisions rather than repeat syntax?

Keep changes small enough to reason about and pair each optimization with evidence. Delete an
optimization when its complexity no longer pays for itself.

## Performance pitfalls

- Optimizing an unmeasured function moves complexity without evidence.
- Timing one run confuses startup/noise with stable behavior.
- Comparing different outputs or workloads invalidates a benchmark.
- Ignoring memory makes a faster implementation fail at realistic size.
- Unbounded caches and concurrency convert speed ideas into resource failures.
- Benchmark assertions on exact time or speed ratios become flaky across CI machines.
- Vectorizing into huge temporaries can be slower and less readable.
- Tuning only a local microbenchmark can worsen end-to-end latency.

## Definition-of-done checklist

- [ ] Behavior, workload, latency/throughput/memory budget, and environment are explicit.
- [ ] A profiler/benchmark identifies the dominant cost before optimization.
- [ ] Reference and optimized outputs match under a justified comparison.
- [ ] Algorithmic complexity and unnecessary work were considered before syntax tricks.
- [ ] Time, memory, readability, freshness, and operational costs are reported.
- [ ] Normal, empty, boundary, invalid, order, mutation, and regression cases are covered as relevant.
- [ ] Format, lint, type, tests, docs, examples, package smoke, and optional checks match the diff.
- [ ] Review has no blocker and production-relevant behavior has monitoring/rollback ownership.

## Run it

```bash
uv run python chapters/12_performance_and_quality/example.py
uv run python chapters/12_performance_and_quality/membership_benchmark_example.py
make check
make wheel-smoke
```

Both micro-timings are illustrative. Compare behavior and order of magnitude on your workload, not an
exact duration printed on another machine.

## Try it

- Benchmark list versus set membership at several sizes, including set-construction time.
- Profile a pandas row loop, then replace it with a vectorized expression and measure memory.
- Add one regression test before optimizing a function.
- Change batch size and report throughput, latency, and peak-memory trade-offs.
- Solve [Prepare tensor batches](../../exercises/hard/11_tensor_batches/README.md).
- Solve [Build a prediction envelope](../../exercises/hard/12_prediction_envelope/README.md).
- Try [Profile a slow feature step](../../docs/exercise-guide.md#challenge-catalog).

## References

- [`timeit`](https://docs.python.org/3/library/timeit.html) — official, free Python microbenchmark
  reference, including command-line and repeated timing behavior.
- [`cProfile` and `profile`](https://docs.python.org/3/library/profile.html) — official, free
  deterministic profiler documentation and interpretation tools.
- [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) — official, free
  guide including the warning that broadcasting can create inefficient memory use.
- [Ruff documentation](https://docs.astral.sh/ruff/) — official, free formatter/linter configuration
  and rule reference; this repository pins a minimum compatible version.
- [pytest documentation](https://docs.pytest.org/) — official, free test, fixture, parametrization, and
  plugin reference.
- [Software Engineering at Google](https://abseil.io/resources/swe-book) — free online book about
  testing, review, and engineering at scale; examples are organizational guidance, not a private
  universal standard.
