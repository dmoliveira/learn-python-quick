# 11 · FastAPI and MLE 🚀

**Time:** 60 minutes · **Prerequisites:** [Types and Pydantic](../03_types_oop_and_pydantic/README.md)
and [ML workflows](../06_ml_workflows_and_metrics/README.md) · **Extra:** `uv sync --dev --extra api`

## Outcomes

You will be able to:

- define typed prediction request and response schemas;
- distinguish transport validation from model validation;
- create `/health` and `/predict` routes with FastAPI;
- test an ASGI app in process without opening a port;
- list the production concerns intentionally absent from a teaching API.

## Make the boundary explicit

An API contract should state field names, units, allowed shapes, response meaning, and model version.
Pydantic rejects malformed input before prediction. A `422` response means request validation failed;
it does not mean a valid-looking measurement is sensible in the real domain.

The course app accepts four Iris measurements and returns a label, confidence, and model version.
It trains a tiny model in memory to avoid unsafe pickle files. This is convenient for learning, not
how a large service should load models.

## Test without a server

FastAPI's test client calls the ASGI application in process. Tests should cover a successful request,
missing/extra/wrong-shape fields, model errors, and health metadata. No core or CI test binds a port.

Production systems additionally need authenticated deployment, artifact integrity, dependency and
data lineage, observability, resource limits, concurrency testing, rollback, drift monitoring,
privacy review, and incident response. Model confidence is not a guarantee of correctness.

## Run it

In-process request:

```bash
uv sync --dev --extra api
uv run python chapters/11_fastapi_and_mle/example.py
```

Optional local server for manual exploration:

```bash
uv run uvicorn learn_python_quick.api:create_app --factory --port 8000
```

Visit `http://127.0.0.1:8000/docs`, then stop the server. The server command is never used in CI.

## Try it

- Send three instead of four features and explain the `422` body.
- Add a batch request limited to 100 rows.
- Add a model-version header and test it in process.
- Try [Add API batch prediction](../../docs/exercise-guide.md#challenge-catalog).

## References

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
