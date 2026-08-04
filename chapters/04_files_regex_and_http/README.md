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

## Run it

```bash
uv run python chapters/04_files_regex_and_http/example.py
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
