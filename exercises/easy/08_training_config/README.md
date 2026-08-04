# 08 · Validate a training configuration 🧪

**Level:** 🟢 Easy · **Time:** 25–40 min · **Read first:**
[Types, OOP, and Pydantic](../../../chapters/03_types_oop_and_pydantic/README.md)

## Problem

Training should fail before expensive work starts when configuration is malformed. Implement
`validate_training_config(payload)` in [`answer.py`](answer.py) with a strict Pydantic v2 model.

```python
payload = {"model_name": " Tiny MLP ", "learning_rate": 0.01, "epochs": 8}
```

Expected result:

```python
{"model_name": "tiny-mlp", "learning_rate": 0.01, "epochs": 8, "seed": 42}
```

### Contract

- Required fields: `model_name`, `learning_rate`, `epochs`; optional `seed` defaults to `42`.
- Forbid every extra field.
- Normalize a nonblank model name with trim, lowercase, and spaces replaced by `-`.
- `learning_rate` must be an actual finite float where `0 < value <= 1`; reject integers and bools.
- `epochs` is a strict integer from 1 to 10,000; `seed` is a strict non-negative integer. Reject bools.
- Return `model_dump()` and do not mutate the input mapping.
- Invalid data must raise Pydantic `ValidationError` with field locations intact.

## Hints

1. Use `ConfigDict(extra="forbid", allow_inf_nan=False)`.
2. `Field(strict=True, ...)` prevents many coercions, but confirm the exact float rule with a
   `field_validator(..., mode="before")`.
3. Pydantic wraps `ValueError` from a field validator into a field-level `ValidationError`.
4. Keep network, file, or model work out of validators.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. Use
> `make exercise-verbose ID=easy/08_training_config` only when you need the full traceback.

```bash
make exercise ID=easy/08_training_config
```

Before revealing the answer, write what static typing proves and what this runtime model proves.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach. Read the
[solution reasoning](../../../solutions/README.md#08--validate-a-training-configuration), then inspect
[`training_config.py`](../../../solutions/easy/training_config.py).

</details>
