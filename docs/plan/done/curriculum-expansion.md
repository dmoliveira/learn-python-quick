# Deep curriculum expansion

Status: completed and validated on 2026-08-04.

## Goal

Deepen every chapter through mental models, gradual code, one worked engineering problem, concrete
pitfalls, completion evidence, and annotated reading. Double the polished exercise set from six to
twelve without repeating existing problems or adding a heavier default environment.

## Delivery slices

1. Chapters 00–04, five core examples, and easy exercises 07–08.
2. Chapters 05–07, two core examples, and medium exercises 09–10.
3. Chapters 08–12, four core/optional examples, and hard exercises 11–12.
4. Navigation, reference ladder, runtime budgets, full optional validation, review, and release.

## Guardrails

- Default examples remain deterministic, offline, and CPU-small.
- Exercises use frozen public contracts and official solutions use the same contracts.
- No model-quality floor is used as an exercise assertion.
- No notebooks, downloads, ports, new dependencies, pretrained models, or private-standard claims.
- `make check` completes within a 60-second core budget; optional tests/examples have a 180-second
  post-install budget.

## Completion evidence

- 13 expanded chapters, 11 additional examples, and 6 additional exercises shipped as planned.
- The final catalog contains 20 core examples, 6 optional examples, and 12 exercises.
- Core, wheel, XGBoost, PyTorch, FastAPI, docs, smoke, contract, and runtime-budget checks passed.
- The final critical review reported no high/medium finding or blocker.
