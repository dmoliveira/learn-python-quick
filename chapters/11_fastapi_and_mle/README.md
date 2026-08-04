# 11 · FastAPI and MLE 🚀

**Time:** 60 minutes · **Prerequisites:** [Types and Pydantic](../03_types_oop_and_pydantic/README.md)
and [ML workflows](../06_ml_workflows_and_metrics/README.md) · **Extra:** `uv sync --dev --extra api`

## Outcomes

You will be able to:

- define typed prediction request and response schemas;
- distinguish transport validation, feature validation, and model behavior;
- create health, single-prediction, and bounded batch routes with FastAPI;
- test an ASGI app in process without opening a port;
- include model version and stable errors in a serving contract;
- list the production concerns intentionally absent from a teaching API.

## Serving is a boundary, not just a route

An inference service turns external bytes into a decision-facing response:

```text
HTTP bytes → parse JSON → validate schema → build features → run model → validate response → HTTP
```

Each arrow can fail differently. Keep transport, domain, feature, and model errors separate enough to
debug and monitor. A successful HTTP status means the service fulfilled its contract; it does not
prove the measurement was collected correctly or the prediction is safe to act on.

## Define the contract before the framework

A request schema should state names, types, units, required/extra fields, and allowed batch shape. A
response schema should state label meaning, score meaning, model/schema version, and ordering.

The course request uses four Iris measurements in centimeters:

```python
class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    features: tuple[float, float, float, float]
```

A tuple encodes exact length. `extra="forbid"` catches a misspelled or unexpected field instead of
silently discarding it. Pydantic validates shape and declared constraints at runtime, but it cannot
know whether a real flower was measured with the correct instrument or whether the API caller is
authorized.

Decide coercion deliberately. Pydantic can convert compatible strings/numbers unless strict fields or
validators forbid it. A public schema change—field rename, unit change, different label set—is an API
change even when the Python function still runs.

## FastAPI connects schemas to HTTP

FastAPI uses type annotations and Pydantic models to parse requests, generate OpenAPI, and serialize
responses. The course app provides:

| Route | Purpose |
|---|---|
| `GET /health` | process health and configured model version |
| `POST /predict` | one four-feature prediction |
| `POST /predict-batch` | 1–100 ordered prediction rows |

Malformed request bodies receive HTTP `422` before route inference runs. An internal model failure is
not a `422`; it should become an appropriate controlled server error and monitoring event without
leaking private stack details.

The response includes label, confidence, and `model_version`. The confidence is the fitted model's
largest class probability, not a guarantee of correctness. Probability calibration and decision
thresholds require separate evaluation.

## Batch requests need explicit bounds

Batching can amortize parsing and model overhead, but an unbounded list lets one request consume
unbounded memory and latency. The course schema requires between 1 and 100 rows:

```python
class BatchPredictionRequest(BaseModel):
    rows: list[PredictionRequest] = Field(min_length=1, max_length=100)
```

The response preserves input order. A production contract must also decide:

- whether one invalid row rejects the whole request or returns per-row errors;
- whether item/request IDs are required for correlation;
- maximum serialized bytes in addition to row count;
- timeout and cancellation behavior;
- whether partial model failures are possible;
- how client retries avoid duplicate side effects.

Prediction is read-only in this example, but logging, billing, or downstream writes can make retries
observable. Design idempotency rather than assuming every POST is harmless.

## Test the ASGI app without a server

FastAPI's `TestClient` calls the ASGI application in the same process. It exercises routing, JSON,
Pydantic, and response serialization without binding a port:

```python
client = TestClient(create_app())
response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
assert response.status_code == 200
```

Cover at least:

- health metadata and model version;
- successful single and ordered batch requests;
- missing, extra, wrong-type, and wrong-length fields;
- empty and over-limit batches;
- controlled model errors and response-schema violations;
- authentication/authorization when those layers exist.

No default or CI test should contact a live host. Network-level tests belong in a separate integration
environment with bounded timeouts and owned dependencies.

## Worked requests

The single-row example calls health and prediction routes in process:

```bash
uv sync --dev --extra api
uv run python chapters/11_fastapi_and_mle/example.py
```

The batch example sends two rows, prints their ordered labels, and confirms an empty batch returns
`422`:

```bash
uv run python chapters/11_fastapi_and_mle/batch_api_example.py
```

Neither command opens a port or performs a network request. The model trains from scikit-learn's
packaged Iris dataset in memory; source, terms, and network behavior are in the
[dataset manifest](../../datasets/manifest.json).

## Model lifecycle belongs outside each request

Loading or training a model for every request wastes latency and resources. The course uses a cached
function so its tiny deterministic model is created once per process. Production startup should:

1. locate an immutable versioned artifact;
2. verify provenance, checksum/signature, and compatible schema;
3. load it with a safe supported format;
4. run a readiness check before receiving traffic;
5. expose the exact version in responses/telemetry;
6. keep the previous version available for rollback.

The course trains in memory to avoid distributing unsafe pickle artifacts. Python pickle/joblib files
can execute code while loading and must not be accepted from untrusted sources.

## Latency, concurrency, and resource limits

Measure end-to-end latency percentiles, not only average model time. Parsing, feature lookup, queueing,
serialization, and downstream calls may dominate inference. Bound request size, in-flight work, model
threads, and timeouts. Add backpressure instead of allowing queues to grow until the process fails.

An `async def` route does not make CPU-heavy inference parallel. CPU work can block an event loop;
process/thread/model-server choices depend on whether the library releases the GIL, batch behavior,
device use, and memory duplication. Load-test the deployed topology with realistic payloads.

## Observability without leaking data

Useful telemetry includes request ID, schema/model version, status/error class, latency, batch size,
resource use, and aggregate prediction/feature drift. Logs and traces should not contain raw private
features by default. Define redaction, access, retention, and deletion policies before collecting.

Monitoring needs action: an owner, alert threshold, runbook, and rollback path. Model-quality labels
often arrive late, so service health, input schema, feature distribution, prediction distribution, and
eventual outcome metrics have different cadences.

## Security and deployment boundaries

Production systems additionally need authentication, authorization, transport security, rate limits,
dependency scanning, least-privilege identities, network policy, secret management, artifact integrity,
privacy review, and incident response. Validate output as well as input, and avoid returning stack
traces or internal artifact paths.

The local server command below is only for manual exploration:

```bash
uv run uvicorn learn_python_quick.api:create_app --factory --host 127.0.0.1 --port 8000
```

Visit `http://127.0.0.1:8000/docs`, then stop the server. It binds only loopback and is never run by
tests or CI. It is not deployment guidance.

## Serving pitfalls

- Loading/training per request creates avoidable latency and failure paths.
- Accepting unbounded batches enables resource exhaustion.
- Returning a model score without version/schema context makes incidents hard to reconstruct.
- Treating `422` as a model error mixes client schema failures with inference failures.
- Using pickle from an untrusted location creates code-execution risk.
- Assuming async syntax solves CPU concurrency leads to event-loop stalls.
- Logging raw features/responses can expose personal or confidential data.
- Shipping without readiness, monitoring, and rollback turns a model into an unmanaged dependency.

## MLE boundary checklist

- [ ] Request/response fields, units, bounds, ordering, and version policy are explicit.
- [ ] Single and batch requests reject malformed/extra input and preserve intended order.
- [ ] Model/artifact loads once, has verified provenance, and reports its version.
- [ ] Health, readiness, latency, errors, batch size, and resource use are observable.
- [ ] Request size, concurrency, threads, timeouts, and backpressure are bounded.
- [ ] Logs/traces follow a privacy-aware field and retention policy.
- [ ] Tests run in process; live integration tests are isolated and bounded.
- [ ] Deployment has authentication, least privilege, rollout, rollback, and an owner.

## Run it

In-process requests:

```bash
uv sync --dev --extra api
uv run python chapters/11_fastapi_and_mle/example.py
uv run python chapters/11_fastapi_and_mle/batch_api_example.py
```

## Try it

- Send three instead of four features and inspect the `422` error location.
- Send 100 and then 101 batch rows and compare status codes.
- Add a request ID to the response and test order/correlation in process.
- Decide whether one invalid row should reject the complete batch and justify the policy.
- Solve [Build a prediction envelope](../../exercises/hard/12_prediction_envelope/README.md).
- Try [Profile batch inference](../../docs/exercise-guide.md#challenge-catalog) without adding a
  fragile speed assertion.

## References

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) — official, free guide to schemas,
  dependencies, errors, and deployment concepts; check the installed version.
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) — official, free in-process
  `TestClient` patterns.
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) — official, free Pydantic v2
  validation, serialization, strictness, and configuration reference.
- [OWASP API Security Top 10](https://owasp.org/API-Security/) — free security-risk catalog; use it
  for threat discovery alongside organization-specific review, not as proof of safety.
- [SLSA specification](https://slsa.dev/spec/) — free supply-chain framework for artifact provenance
  and build integrity; implementation depth depends on release risk.
