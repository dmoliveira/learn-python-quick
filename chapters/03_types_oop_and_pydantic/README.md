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

## Three different contracts

It helps to separate what each layer can prove:

| Layer | Example | What it proves |
|---|---|---|
| Static type | `Sequence[float]` | Code is used consistently according to the checker |
| Runtime shape | Pydantic field constraints | Incoming data has the declared fields/types/ranges |
| Domain invariant | “features were measured before prediction time” | A business fact your code and process must establish |

Mypy does not inspect production JSON. Pydantic does not know that a clinical measurement was taken
correctly. A class name does not guarantee a good abstraction.

## Composition before inheritance

Inheritance is useful for true substitutable relationships, but it also couples subclasses to base
implementation details. Composition builds an object from smaller collaborators:

```text
validated request → Predictor protocol → Prediction value → response formatter
```

A protocol describes behavior. A production model and a deterministic fake can satisfy the same
protocol without sharing a parent class. Tests stay small because the fake does not load a model.

## Worked problem: prediction boundary

[`prediction_boundary_example.py`](prediction_boundary_example.py) accepts an untrusted dictionary:

1. `PredictionPayload.model_validate` checks the external shape and rejects extra fields.
2. `handle_prediction` depends on `Predictor`, not a concrete model.
3. `FixedPredictor` structurally satisfies the protocol.
4. The response contains plain serializable data.
5. An invalid payload produces field-level Pydantic errors before model code runs.

```bash
uv run python chapters/03_types_oop_and_pydantic/prediction_boundary_example.py
```

## Pydantic v2 details worth knowing

- Use `model_validate` for Python input and `model_validate_json` for JSON text.
- Use `model_dump` for a dictionary and `model_dump_json` for JSON output.
- `extra="forbid"` detects misspelled or unexpected fields instead of silently dropping them.
- Strict fields reject coercion when accepting `"10"` as `10` would hide an upstream bug.
- Validators should normalize one boundary fact, not perform database or network work.

Many online snippets still use Pydantic v1's `parse_obj` or `.dict()`. Check the migration guide
before copying them.

## Typed-design pitfalls

- `Any` turns off useful checking and spreads quickly across boundaries.
- A large “manager” class often hides several independent responsibilities.
- Deep inheritance makes construction/testing harder and substitution less clear.
- Runtime validation on every internal function can duplicate work; validate at boundaries.
- Serialization is a public contract: renaming fields can break clients and stored artifacts.

## Typed-design checklist

- [ ] Static, runtime, and domain contracts are distinguished.
- [ ] Boundary input rejects unknown fields when appropriate.
- [ ] Internal values are immutable when mutation is not required.
- [ ] Collaborators depend on small protocols, not implementation details.
- [ ] A fake can exercise orchestration without loading external resources.
- [ ] Serialization/version changes are treated as API changes.

## Run it

```bash
uv run python chapters/03_types_oop_and_pydantic/example.py
uv run python chapters/03_types_oop_and_pydantic/prediction_boundary_example.py
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
- [Pydantic v2 migration guide](https://docs.pydantic.dev/latest/migration/) — official mapping from
  common v1 APIs to current syntax.
- [Architecture Patterns with Python](https://www.cosmicpython.com/book/preface.html) by Harry
  Percival and Bob Gregory — free online edition about boundaries, protocols, and composition.
