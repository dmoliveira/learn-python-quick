# 01 · Python fundamentals 🐍

**Time:** 45 minutes · **Prerequisites:** [Start here](../00_start_here/README.md)

## Outcomes

You will be able to:

- use values, variables, expressions, and clear names;
- write functions with positional, default, and keyword-only arguments;
- choose `if`, `for`, `while`, and `match` for control flow;
- raise and catch specific exceptions at useful boundaries;
- separate pure calculation from input/output.

## Core ideas

Python names point to objects. Assignment does not copy a list or dictionary. Use immutable values
when mutation would be surprising, and return a new result when practical.

Functions should have one visible purpose. This signature makes the fallback explicit:

```python
def safe_divide(
    numerator: float,
    denominator: float,
    *,
    default: float = 0.0,
) -> float:
    return default if denominator == 0 else numerator / denominator
```

The `*` makes `default` keyword-only: `safe_divide(2, 0, default=-1)`. Use `/` for positional-only
arguments when the parameter name is not part of the public contract. Do not use mutable default
values such as `items=[]`; create the list inside the function instead.

### Control flow guide

| Need | Prefer |
|---|---|
| Choose between conditions | `if` / `elif` / `else` |
| Visit each item | `for` |
| Repeat until a state changes | `while`, with an obvious exit |
| Match a small known shape/state | `match` |
| Transform/filter a short sequence | a readable comprehension |

Catch the exception you can handle. Avoid `except Exception:` around large blocks because it hides
programming errors. A useful error says what was invalid and what the caller should change.

## Names, values, and mutation

Assignment binds another name to the same object. It does not copy a mutable value:

```python
original = ["view"]
alias = original
alias.append("buy")
assert original == ["view", "buy"]
```

Use `list(original)`, `original.copy()`, or a deeper copy only when a separate object is part of the
contract. Copying everything defensively is also costly and can hide unclear ownership. A better
question is: **which function owns mutation?**

Immutable values such as strings, integers, tuples, and frozen dataclasses make shared state easier
to reason about. A tuple can still contain a mutable object, so immutability is about the whole object
graph, not only the outer type.

## Pure core, imperative shell

A **pure function** returns a result from its arguments without changing external state. The
**imperative shell** reads files, sends requests, prints, and coordinates those functions.

```text
parse input → validate → calculate quote → format response
```

This separation makes calculation tests fast and deterministic. It also keeps display choices—such
as currency formatting—out of business rules.

## Worked problem: order quote

[`order_quote_example.py`](order_quote_example.py) uses `Decimal` for money, a positional-only items
argument, and keyword-only discount settings. The calculation validates each line, returns values,
and never prints. A second function formats the result.

Read it in this order:

1. `LineItem` describes the dictionary shape for the type checker.
2. `calculate_quote` protects quantity, price, SKU, and discount invariants.
3. The threshold branch calculates one discount; no I/O occurs.
4. `format_quote` owns presentation.
5. The example copies input only to prove the function did not mutate it.

```bash
uv run python chapters/01_python_fundamentals/order_quote_example.py
```

## Common traps

- **Mutable default arguments:** one list can be shared across calls. Default to `None`, then create.
- **Boolean as integer:** `bool` is a subclass of `int`; validate explicitly when `True` is invalid.
- **Float money:** binary floats cannot represent every decimal fraction exactly. Use integer minor
  units or `Decimal` when exact accounting matters.
- **Catching too much:** broad exception handling can turn a bug into wrong output.
- **Dense one-liners:** a clever comprehension is not better when branches or side effects obscure it.

## Foundation engineering checklist

- [ ] Signature makes optional and keyword-only choices clear.
- [ ] Inputs and invalid values are documented.
- [ ] Mutation ownership is explicit.
- [ ] Calculation is separate from I/O/formatting.
- [ ] Error messages tell callers what to change.
- [ ] Normal, empty, boundary, and invalid cases have evidence.

## Run it

```bash
uv run python chapters/01_python_fundamentals/example.py
uv run python chapters/01_python_fundamentals/order_quote_example.py
```

Read [`foundations.py`](../../src/learn_python_quick/foundations.py) after predicting the output.

## Try it

- Add a `CANCELED` job state and decide its next action.
- Make `format_metric` reject more than ten decimal places.
- Solve [Summarize café sales](../../exercises/easy/01_sales_summary/README.md).

## References

- [Python control flow](https://docs.python.org/3/tutorial/controlflow.html)
- [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
- [PEP 8 naming and programming recommendations](https://peps.python.org/pep-0008/)
- [Effective Python](https://effectivepython.com/) by Brett Slatkin — paid book; practical guidance
  on function APIs, comprehensions, generators, and maintainable Python.
- [Python language reference](https://docs.python.org/3/reference/) — precise free reference for
  object, expression, and execution semantics when the tutorial is not detailed enough.
