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

## Run it

```bash
uv run python chapters/02_data_structures_and_iteration/example.py
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
