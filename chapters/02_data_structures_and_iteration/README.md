# 02 · Data structures and iteration 🧰

**Time:** 45 minutes · **Prerequisites:** [Python fundamentals](../01_python_fundamentals/README.md)

## Outcomes

You will be able to:

- choose lists, tuples, dictionaries, and sets by behavior;
- write readable comprehensions and generator expressions;
- use `Counter`, `defaultdict`, `deque`, and `dataclass`;
- combine lazy iterators with `itertools`;
- avoid accidental quadratic work and unnecessary copies.

## Pick by operation

| Structure | Best fit | Typical cost |
|---|---|---|
| `list` | ordered, mutable sequence | append O(1), membership O(n) |
| `tuple` | small immutable record/sequence | membership O(n) |
| `dict` | key → value lookup | lookup O(1) average |
| `set` | uniqueness and membership | membership O(1) average |
| `deque` | add/remove at both ends | O(1) at either end |

Big-O is not a stopwatch. Small inputs may favor simple code, but repeated `item in large_list` is a
signal that a set may express the intent better.

### Lazy iteration

A list comprehension creates all results now. A generator expression yields one result at a time:

```python
total = sum(row["amount"] for row in rows if row["status"] == "paid")
```

Useful `itertools` tools include `chain`, `islice`, `pairwise`, `product`, and `groupby`. Note that
`groupby` groups adjacent values; sort first when the data is not already grouped. The standard
library's `collections` and `itertools` often replace custom loops with tested vocabulary.

## Iterable is not iterator

An **iterable** can produce an iterator. An **iterator** remembers its current position and is
consumed as values are requested.

```python
numbers = [1, 2, 3]  # iterable: can be iterated many times
cursor = iter(numbers)  # iterator: one moving cursor
assert next(cursor) == 1
assert list(cursor) == [2, 3]
assert list(cursor) == []
```

This matters for files, generators, database cursors, and model batches. If you need two passes,
either recreate the iterator, materialize bounded data, or redesign to finish in one pass.

## Determinism and grouping

Sets and dictionaries provide fast membership/lookup, but ranking still needs an explicit order.
Use a final key such as `(-count, item_id)` so equal counts do not depend on input or hash order.

`itertools.groupby` groups **adjacent** equal keys. To group all records for a user, first establish a
user/time ordering—or use a dictionary when preserving streaming order is more important than
sorting.

## Worked problem: session windows

[`session_window_example.py`](session_window_example.py) turns user events into sessions separated by
more than 30 minutes:

1. Sort by `(user_id, occurred_at)` to define deterministic adjacency.
2. Use `groupby` to receive one user's iterator.
3. Materialize only that user's small group because `pairwise` and a second pass are needed.
4. Mark a new session when the time gap exceeds the contract.
5. Use a bounded `deque` separately for recent activity.

```bash
uv run python chapters/02_data_structures_and_iteration/session_window_example.py
```

At large scale you may sort upstream, partition by user, and stream one partition at a time. The
algorithmic question comes before a library choice.

## Complexity you should notice

- Repeated `item in list` inside a loop can become O(n²); prebuild a set when order is not needed.
- Sorting is usually O(n log n) and requires memory; avoid it when data already has a trusted order.
- `list(generator)` removes laziness and can exhaust memory on unbounded input.
- A dictionary lookup is O(1) on average, not a promise for every adversarial case.

## Collection engineering checklist

- [ ] Structure matches the dominant operation: order, lookup, uniqueness, or queueing.
- [ ] Iterator consumption and number of passes are intentional.
- [ ] Ranking/grouping has deterministic order and tie rules.
- [ ] Bounded state is used for streams where possible.
- [ ] Expected time and memory growth are explained.
- [ ] Empty and duplicate inputs are covered.

## Run it

```bash
uv run python chapters/02_data_structures_and_iteration/example.py
uv run python chapters/02_data_structures_and_iteration/session_window_example.py
```

## Try it

- Change the event stream and inspect how `Counter` and `deque(maxlen=...)` react.
- Rewrite the pairwise differences once with indexing and once with `itertools.pairwise`.
- Explain why `set(events)` loses information needed by the counter.
- Continue to [Types, OOP, and Pydantic](../03_types_oop_and_pydantic/README.md).

## References

- [Built-in data types](https://docs.python.org/3/library/stdtypes.html)
- [`collections`](https://docs.python.org/3/library/collections.html)
- [`itertools`](https://docs.python.org/3/library/itertools.html)
- [Problem Solving with Algorithms and Data Structures using Python](https://runestone.academy/ns/books/published/pythonds3/index.html)
  — free book for Big-O reasoning and classic structure trade-offs.
