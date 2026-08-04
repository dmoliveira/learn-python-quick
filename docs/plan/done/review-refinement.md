# Review refinement plan

Status: implemented and validated on 2026-08-04.

## Goal

Improve how learners start, track progress, recover from exercise failures, and understand important
evaluation boundaries without expanding the curriculum or default dependency footprint.

## Batch A · Start, track, recover

- Add a path-safe exercise runner with concise default feedback and a verbose mode.
- Start every learning route at Chapter 00 and add one Markdown progress checklist.
- Point the CLI and README to the orientation and checklist.
- Test runner exit codes, path containment, CLI output, and public performance helpers.

## Batch B · Honest boundaries

- Validate regression, binary classification, attention, and text-search inputs explicitly.
- Add UTC timestamps and a deterministic temporal recommender split aligned to training candidates.
- Evaluate the chapter recommender against future unseen items rather than a hard-coded label.
- Keep generated data offline and update its manifest checksum.

## Gates

Run targeted tests after each batch. Final gates are `make check` under the documented 60-second
budget, `make wheel-smoke`, dataset reproduction, Python 3.11–3.13 CI, wheel and optional CI jobs, and
implementation plus learner-experience review with no blocker.
