# 12 · Build a prediction envelope 📦

**Level:** 🔴 Hard · **Time:** 85–120 min · **Read first:**
[Types, OOP, and Pydantic](../../../chapters/03_types_oop_and_pydantic/README.md) and
[FastAPI and MLE](../../../chapters/11_fastapi_and_mle/README.md)

## Problem

A serving boundary needs a strict, serializable batch response. Implement
`build_prediction_envelope(predictions, request_id, model_version)` in [`answer.py`](answer.py).

Each input prediction has exactly these fields:

```python
{"item_id": "row-1", "label": "review", "confidence": 0.82}
```

Return:

```python
{
    "request_id": "req-7",
    "model_version": "risk-v3",
    "predictions": [
        {"item_id": "row-1", "label": "review", "confidence": 0.82},
    ],
    "label_counts": {"review": 1},
}
```

The envelope is plain Python data ready for JSON serialization. It does not start a server or run a
model.

### Contract

- Accept zero through 100 prediction mappings and preserve their order.
- Each prediction must contain exactly `item_id`, `label`, and `confidence`.
- `request_id`, `model_version`, `item_id`, and `label` must be strict, non-blank strings. Strip
  surrounding whitespace in the returned data.
- Item IDs must be unique after stripping whitespace.
- Confidence must be a Python `float`, finite, and from `0.0` through `1.0`. Reject integers,
  booleans, strings, `NaN`, and infinities rather than coercing them.
- Reject extra or missing prediction fields.
- Return exactly `request_id`, `model_version`, `predictions`, and `label_counts`.
- Sort `label_counts` alphabetically by label. For no predictions, return an empty prediction list
  and empty counts.
- Raise Pydantic `ValidationError` for every validation failure.
- Do not mutate the input sequence or any prediction mapping.

## Design guidance

Use private Pydantic models inside your answer. One model can validate an item and another can
validate the request metadata, bounded list, and unique IDs. After validation, build the derived
`label_counts` field and call `model_dump()` on each prediction.

Strict validation is intentional at an API boundary. Accepting confidence `1` or `"0.8"` would hide
an upstream schema change. Validation still cannot prove a confidence is calibrated or a label is
appropriate for a real decision.

## Hints

1. Set `ConfigDict(extra="forbid", strict=True)` on both models.
2. Use a `field_validator(..., mode="before")` to check the exact input type and normalize strings.
3. A separate `mode="before"` confidence validator can reject non-floats and non-finite values.
4. Use `Field(max_length=100)` on the prediction list.
5. A `model_validator(mode="after")` can compare the number of IDs with the number of unique IDs.
6. Count labels only after the complete envelope has validated.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=hard/12_prediction_envelope
```

Before opening the answer, test a duplicate ID that differs only by surrounding whitespace and a
confidence supplied as integer `1`. Explain why both should be rejected or normalized as specified.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#12--build-a-prediction-envelope), then inspect
[`prediction_envelope.py`](../../../solutions/hard/prediction_envelope.py).

</details>
