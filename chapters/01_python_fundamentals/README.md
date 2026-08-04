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

## Run it

```bash
uv run python chapters/01_python_fundamentals/example.py
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
