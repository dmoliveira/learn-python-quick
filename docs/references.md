# Reference ladder

Use a reference to answer a question, then return to code and test the claim. Prefer the documentation
for the version installed by `uv.lock`; web examples can target older APIs.

Labels on this page mean:

- **Official · free:** maintained by the language/library/project.
- **Primary · free:** original specification, standard, paper, or dataset source.
- **Community · free:** public teaching material; useful context, not an API contract.
- **Book · free/paid:** longer treatment; “paid” means access may require purchase/subscription.

Public company guides describe public guidance, not private engineering standards. A source being
listed does not make every recommendation appropriate for every product or risk level.

## 00 · Start, tools, and the learning loop

- [Python tutorial](https://docs.python.org/3/tutorial/) — **Official · free.** Use it to refresh syntax
  and the interpreter model; this course supports Python 3.11–3.13.
- [uv documentation](https://docs.astral.sh/uv/) — **Official · free.** Environment, lockfile, Python,
  dependency, and build commands used by this repository.
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html) — **Official · free.**
  Test discovery, assertions, and failure output used in the run-change-test loop.

## 01 · Python fundamentals

- [Python language reference](https://docs.python.org/3/reference/) — **Official · free.** Precise
  semantics for expressions, statements, functions, and exceptions when the tutorial is not enough.
- [Built-in functions](https://docs.python.org/3/library/functions.html) — **Official · free.** Check
  signatures and edge behavior before writing a custom helper.
- [PEP 8](https://peps.python.org/pep-0008/) — **Primary · free.** Python style guidance; the repository
  formatter/linter remains the executable local policy.
- [Effective Python, 3rd edition](https://effectivepython.com/) by Brett Slatkin — **Book · paid.**
  Focused engineering patterns; confirm edition because examples evolve with Python.

## 02 · Data structures and iteration

- [Built-in types](https://docs.python.org/3/library/stdtypes.html) — **Official · free.** List, tuple,
  range, string, set, dictionary, view, and operation semantics.
- [`collections`](https://docs.python.org/3/library/collections.html) and
  [`itertools`](https://docs.python.org/3/library/itertools.html) — **Official · free.** Reusable
  containers and lazy iterator building blocks.
- [Iterator protocol](https://docs.python.org/3/library/stdtypes.html#iterator-types) — **Official ·
  free.** The exact iterable/iterator contract and exhaustion behavior.
- [Fluent Python, 2nd edition](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) by
  Luciano Ramalho — **Book · paid.** Deep treatment of Python's data model and iteration.

## 03 · Types, OOP, and Pydantic

- [Python typing specification](https://typing.python.org/en/latest/spec/) — **Official · free.**
  Structural typing, protocols, generics, and checker-facing semantics.
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) — **Official · free.** Generated
  value-object methods, frozen behavior, fields, and inheritance details.
- [Pydantic v2 models](https://docs.pydantic.dev/latest/concepts/models/) and
  [migration guide](https://docs.pydantic.dev/latest/migration/) — **Official · free.** Runtime
  validation/serialization and the v1-to-v2 API differences common in copied snippets.
- [Architecture Patterns with Python](https://www.cosmicpython.com/book/preface.html) by Harry Percival
  and Bob Gregory — **Book · free online.** Composition, boundaries, repositories, and testable
  architecture; use selectively for a small course project.

## 04 · Files, regex, and HTTP

- [`pathlib`](https://docs.python.org/3/library/pathlib.html), [`json`](https://docs.python.org/3/library/json.html),
  [`csv`](https://docs.python.org/3/library/csv.html), and [`re`](https://docs.python.org/3/library/re.html) —
  **Official · free.** Primary APIs for the chapter's local boundaries.
- [Requests quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/) — **Official ·
  free.** Timeouts, status handling, sessions, and JSON responses; the course tests use injected fakes.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — **Primary · free.** Method,
  status, and HTTP semantic definitions when framework summaries are ambiguous.
- [OWASP input validation cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) —
  **Community · free.** Threat-oriented validation guidance; it does not replace a product threat model.

## 05 · NumPy and pandas

- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) and
  [broadcasting rules](https://numpy.org/doc/stable/user/basics.broadcasting.html) — **Official ·
  free.** Shape, axis, indexing, dtype, vectorization, and memory warnings.
- [pandas getting started](https://pandas.pydata.org/docs/getting_started/index.html) — **Official ·
  free.** Selection, grouped calculations, reshaping, missing values, and table workflows.
- [pandas merge guide](https://pandas.pydata.org/docs/user_guide/merging.html) — **Official · free.**
  Join type, cardinality validation, indicators, concatenation, and copy behavior.
- [Python for Data Analysis, 3E](https://wesmckinney.com/book/) by Wes McKinney — **Book · free
  online.** Longer NumPy/pandas workflows from pandas' creator; examples target the listed edition.

## 06 · ML workflows and metrics

- [scikit-learn model selection](https://scikit-learn.org/stable/model_selection.html),
  [model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html), and
  [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) — **Official · free.** Split,
  cross-validation, metric, pipeline, inconsistent-preprocessing, and leakage behavior.
- [scikit-learn pipelines](https://scikit-learn.org/stable/modules/compose.html#pipeline) — **Official ·
  free.** Fit transformations inside each training fold and compose heterogeneous columns.
- [An Introduction to Statistical Learning with Python](https://www.statlearning.com/) — **Book · free
  PDF / paid print.** Statistical learning, resampling, regression, classification, and trees.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — **Community ·
  free.** Public production lessons about baselines and pipelines; not a universal or private standard.

## 07 · Trees and XGBoost

- [scikit-learn decision trees](https://scikit-learn.org/stable/modules/tree.html) and
  [ensemble methods](https://scikit-learn.org/stable/modules/ensemble.html) — **Official · free.**
  Capacity controls, forests, gradient boosting, advantages, and limitations.
- [XGBoost Python API](https://xgboost.readthedocs.io/en/stable/python/python_api.html) and
  [parameter guide](https://xgboost.readthedocs.io/en/stable/parameter.html) — **Official · free.**
  Use the docs matching the installed supported version range; early-stopping examples vary by release.
- [Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/) by Christoph
  Molnar — **Book · free online.** Permutation importance, local explanations, interactions, and
  limitations; explanation is not causality.

## 08 · PyTorch and images

- [PyTorch tensors](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html),
  [autograd](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html), and
  [optimization](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) —
  **Official · free.** The exact concepts used by the optional examples.
- [PyTorch reproducibility](https://pytorch.org/docs/stable/notes/randomness.html) — **Official · free.**
  Seed, deterministic-operation, platform, and release caveats.
- [Dive into Deep Learning](https://d2l.ai/) — **Book · free online.** Broader theory and executable
  examples; framework/API versions may differ from this repository.
- [scikit-learn Digits data](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset) —
  **Official · free.** Source description for the packaged image fixture.

## 09 · Embeddings and transformers

- [scikit-learn text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) —
  **Official · free.** TF-IDF baseline construction and sparse feature behavior.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — **Primary · free.** Original
  transformer paper; current architectures and implementations differ.
- [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) — **Community ·
  free.** Equation-to-code walkthrough; check the page's stated framework version.
- [PyTorch transformer building blocks](https://pytorch.org/tutorials/intermediate/transformer_building_blocks.html) —
  **Official · free.** Current framework components and performance considerations.
- [Sentence Transformers evaluation](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html) —
  **Official · free.** Evaluator catalog for a popular optional ecosystem; the course does not install
  or download its pretrained models.

## 10 · Recommenders

- [Google recommendation systems guide](https://developers.google.com/machine-learning/recommendation) —
  **Community · free.** Public candidate-generation, scoring, and reranking overview.
- [NDCG in scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html) —
  **Official · free.** One concrete graded-ranking implementation and input convention.
- [Recommender Systems Handbook](https://link.springer.com/book/10.1007/978-1-0716-2197-4) — **Book ·
  paid.** Edited coverage of algorithms, evaluation, and system concerns; verify edition access.
- [GroupLens MovieLens datasets](https://grouplens.org/datasets/movielens/) — **Primary · free with
  separate terms.** Dataset source and usage conditions; this course does not download MovieLens.

## 11 · FastAPI and MLE

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) and
  [testing guide](https://fastapi.tiangolo.com/tutorial/testing/) — **Official · free.** Request,
  response, dependency, error, OpenAPI, and in-process test behavior.
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) — **Official · free.**
  Decide whether a boundary should coerce or reject compatible-looking data.
- [OWASP API Security Top 10](https://owasp.org/API-Security/) — **Community · free.** Risk discovery
  for authorization, resource limits, inventory, and unsafe API consumption; not proof of safety.
- [SLSA specification](https://slsa.dev/spec/) — **Primary · free.** Supply-chain levels and artifact
  provenance concepts for higher-risk release systems.
- [Designing Machine Learning Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) by
  Chip Huyen — **Book · paid.** Data, serving, monitoring, and continual-system trade-offs.

## 12 · Performance and quality

- [`timeit`](https://docs.python.org/3/library/timeit.html) and
  [`cProfile`](https://docs.python.org/3/library/profile.html) — **Official · free.** Repeatable local
  timing and deterministic profiling tools.
- [Ruff documentation](https://docs.astral.sh/ruff/) — **Official · free.** Formatter/linter rules and
  configuration used by the repository.
- [pytest documentation](https://docs.pytest.org/) — **Official · free.** Fixtures, parametrization,
  assertions, markers, and plugins used by the tests.
- [Software Engineering at Google](https://abseil.io/resources/swe-book) — **Book · free online.**
  Public review/testing/maintenance practices from one organization, not a private universal standard.

## Dataset and license checks

- [scikit-learn toy datasets](https://scikit-learn.org/stable/datasets/toy_dataset.html) — **Official ·
  free.** Loader descriptions and original attributions for core packaged datasets.
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/) — **Primary · free with dataset-level
  terms.** Original source for several classic datasets; inspect each dataset's conditions.
- [Local dataset guide](datasets.md) and [manifest](../datasets/manifest.json) — course source, terms,
  redistribution, network behavior, generation details, and fixture checksums.

Library licenses are linked from upstream projects. Dataset and model terms are independent from code
licenses. Check redistribution, commercial-use, attribution, privacy, and update requirements before
using any external data or pretrained artifact.
