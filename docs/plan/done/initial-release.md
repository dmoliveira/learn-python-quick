# Initial release plan

Status: approved for implementation on 2026-08-04.

## Goal

Ship a concise but broad first release that lets software engineers review modern Python and follow
an offline-default, CPU-friendly path into Data Science and Machine Learning Engineering.

## Slices and gates

1. **Foundation:** repository UX, tooling, chapter contracts, core Python modules, starter integrity.
2. **Data and classical ML:** NumPy/pandas, metrics, leakage-safe pipelines, packaged datasets.
3. **Advanced MLE:** isolated XGBoost/PyTorch/FastAPI extras, attention, images, recommenders.
4. **Release:** six polished exercises and solutions, wheel smoke, CI matrix, review, public PR.

The default repository suite must stay green with untouched learner starters. Learner-facing tests
and official solutions share public behavioral contracts. Optional libraries are tested separately
on Python 3.12 and are never imported from the core package initializer.

## Budgets

- Core gate: under 60 seconds per supported Python on a typical CI runner.
- Full optional gate: under 3 minutes after dependency installation.
- No default download, API key, bound port, GPU requirement, or exact cross-platform float claim.

## Review decision

Plan review approved after adding separate test paths, optional dependency boundaries, clean-wheel
execution, dataset provenance, network blocking, tolerant metric assertions, and factual README
claims. The advanced chapters stay short; six exercises receive full contracts and explanations.
