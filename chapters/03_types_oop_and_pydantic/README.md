# 03 · Types, OOP, and Pydantic 🧩

**Time:** 55 minutes · **Prerequisites:** Chapters [01](../01_python_fundamentals/README.md) and
[02](../02_data_structures_and_iteration/README.md)

## Outcomes

You will be able to:

- annotate collections, unions, returns, and callable contracts;
- use dataclasses for small value objects and Pydantic for external input;
- design classes around invariants and composition;
- use a `Protocol` for structural interfaces;
- distinguish static type checking from runtime validation.

## Types communicate contracts

Type hints help editors, reviewers, and tools. Python does not enforce them at runtime. Keep public
annotations precise and let local inference handle obvious temporary values.

```python
class Predictor(Protocol):
    def predict_one(self, features: Sequence[float]) -> Prediction: ...
```

Any object with that method can satisfy the protocol—no inheritance is required. This supports
small fakes in tests and reduces coupling.

### Choose the right model

| Tool | Use it for |
|---|---|
| plain function | stateless transformation |
| `TypedDict` | typed dictionary shape without runtime behavior |
| `dataclass` | internal value object with generated methods |
| Pydantic `BaseModel` | untrusted JSON/config/request validation |
| regular class | identity, lifecycle, invariants, or coordinated behavior |

Prefer composition over a deep inheritance tree. A class is useful when data and behavior protect an
invariant together—not simply because the language supports classes.

Pydantic v2 validates at runtime and can reject unknown fields with `ConfigDict(extra="forbid")`.
Validation does not make a value true or safe; it only proves the declared shape and constraints.

## Run it

```bash
uv run python chapters/03_types_oop_and_pydantic/example.py
uv run mypy src
```

## Try it

- Add a `batch_size` field constrained to 1–4096.
- Create a fake predictor that always returns a known result; pass it to `describe_prediction`.
- Compare a frozen Pydantic model with a frozen dataclass.
- Continue to [Files, regex, and HTTP](../04_files_regex_and_http/README.md).

## References

- [Python typing](https://docs.python.org/3/library/typing.html)
- [Typing protocols](https://typing.python.org/en/latest/spec/protocol.html)
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
