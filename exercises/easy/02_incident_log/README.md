# 02 · Triage incident logs 🚨

**Level:** 🟢 Easy · **Time:** 25–35 min · **Read first:**
[Files, regex, and HTTP](../../../chapters/04_files_regex_and_http/README.md)

## Problem

An on-call engineer needs only `ERROR` and `CRITICAL` events from a service log. Implement
`triage_incidents(lines)` in [`answer.py`](answer.py).

Valid lines have this exact shape:

```text
2026-08-04T09:01:12Z ERROR payments provider timeout
```

Return a dictionary with an ordered `incidents` list and an `invalid_lines` count. Each incident is a
dictionary with `timestamp`, `level`, `service`, and `message`.

### Contract

- Recognize levels `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
- Keep only `ERROR` and `CRITICAL`, preserving input order.
- Count malformed non-empty lines. Ignore blank lines.
- Require a UTC timestamp ending in `Z`, a lowercase service name, and a non-empty message.
- Empty input returns empty incidents and zero invalid lines.

Try the generated [`incidents.log`](../../../datasets/generated/incidents.log).

## Hints

1. Compile one regex outside the loop and use named groups.
2. Use `fullmatch`, not a partial search.
3. Parse and filter are different steps: valid `INFO` is not invalid.
4. Start with the test's smallest example before reading the fixture.

## Check your work

> **Expected first result:** an untouched starter raises `NotImplementedError`. That means the
> learner check is working. Run `make check` when you want the green repository-health check.

```bash
make exercise ID=easy/02_incident_log
```

Before opening the answer, list one valid ignored line and one malformed line.

<details>
<summary>Reveal the reference solution after attempting</summary>

This is one valid approach, not the only possible answer. Read the
[explanation](../../../solutions/README.md#02--triage-incident-logs), then inspect
[`incident_log.py`](../../../solutions/easy/incident_log.py).

</details>
