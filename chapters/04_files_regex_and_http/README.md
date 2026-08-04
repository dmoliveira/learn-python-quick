# 04 · Files, regex, and HTTP 🗂️

**Time:** 60 minutes · **Prerequisites:** Chapters [01](../01_python_fundamentals/README.md)–[03](../03_types_oop_and_pydantic/README.md)

## Outcomes

You will be able to:

- navigate files safely with `pathlib` and context managers;
- stream CSV/JSONL instead of loading unknown-size files;
- design and test a regular expression with named groups;
- call HTTP with timeouts, status checks, and injected sessions;
- add context to parsing errors without hiding their cause.

## Boundaries fail differently

Files may be missing, malformed, too large, or encoded differently. HTTP can fail before connecting,
return a non-success status, or return unexpected JSON. Validate at the boundary and keep the inner
calculation independent from I/O.

```python
path = Path("events.jsonl")
with path.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, start=1):
        ...
```

`with` closes the file even when parsing raises. JSONL keeps one JSON object per line, which is easy
to stream and inspect.

### Regex checklist

1. Start with a plain string method when it is enough.
2. Anchor the full contract with `^...$` or `fullmatch`.
3. Use raw strings and named groups.
4. Test normal, boundary, malformed, and adversarially long text.
5. Avoid nested ambiguous quantifiers that can cause catastrophic backtracking.

Every Requests call needs an explicit timeout. Call `raise_for_status()` before trusting the body.
Inject a session or transport in tests; core tests never contact a live service.

## Design a boundary pipeline

Reliable boundary code does a few explicit steps:

```text
locate resource → open/connect → read bytes/text → parse shape → validate meaning → calculate
```

Keep these steps visible. “File not found,” “invalid JSON,” and “valid JSON with a missing field” are
different failures and need different context. Wrap an exception only when you can add useful domain
information, and preserve the original with `raise ... from error`.

## Streaming and atomic output

JSONL and CSV can be processed one record at a time. Streaming controls memory but also changes error
timing: malformed line 50,000 appears only when iteration reaches it.

For important output, write to a temporary file in the same filesystem, flush/close it, then replace
the destination. This avoids leaving a half-written final file after a crash. The small course writer
creates parent directories but intentionally does not claim transactional durability.

## Worked problem: JSONL quality report

[`jsonl_quality_example.py`](jsonl_quality_example.py) uses a temporary directory, writes two typed
log events, reads them lazily, appends malformed text, and proves the parser reports line 3.

```bash
uv run python chapters/04_files_regex_and_http/jsonl_quality_example.py
```

The temporary directory keeps the example repeatable and leaves no repository state. The calculation
does not depend on a live service or a user's home directory.

## HTTP decisions beyond `get()`

- **Timeout:** use a finite connect/read budget; a default of “forever” is unsafe.
- **Status:** 4xx usually means changing the request; 5xx may be transient.
- **Retry:** retry only operations safe to repeat, with bounded attempts and backoff.
- **Idempotency:** GET is designed to be repeatable; POST may need an idempotency key.
- **Session:** reuse connections when many requests target one service.
- **Contract:** validate content type and body shape before business logic.

Tests should inject a fake response for success, timeout, status error, and malformed JSON. Live tests
belong in an explicit integration job because uptime and rate limits are outside unit-test control.

## Regex failure modes

- A loose search can accept a valid substring inside invalid text; prefer `fullmatch` for contracts.
- `.*` can consume more than expected; use precise character classes.
- Nested ambiguous repetition can cause catastrophic backtracking on long input.
- Regex is a parser for regular text shapes, not a good replacement for JSON/HTML/SQL parsers.

## Boundary engineering checklist

- [ ] Paths are `Path` objects and encoding is explicit.
- [ ] Files/resources close on success and failure.
- [ ] Large input can stream or has a documented size limit.
- [ ] Parse errors include line/record context.
- [ ] HTTP calls have timeout, status handling, and an injectable transport.
- [ ] Retry safety and maximum attempts are explicit.
- [ ] Tests make no real network call by default.

## Run it

```bash
uv run python chapters/04_files_regex_and_http/example.py
uv run python chapters/04_files_regex_and_http/jsonl_quality_example.py
```

The HTTP response in this example is a fake. No network call occurs.

## Try it

- Add a new log level and test it before changing the regex.
- Write parsed incidents to temporary JSONL, then read them back.
- Make the fake response return a list and observe the boundary error.
- Solve [Triage incident logs](../../exercises/easy/02_incident_log/README.md).

## References

- [`pathlib`](https://docs.python.org/3/library/pathlib.html)
- [`json`](https://docs.python.org/3/library/json.html) and [`csv`](https://docs.python.org/3/library/csv.html)
- [`re`](https://docs.python.org/3/library/re.html)
- [Requests quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — free primary reference for
  methods, status codes, and request/response meaning.
