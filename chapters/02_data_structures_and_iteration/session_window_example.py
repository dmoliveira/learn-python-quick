"""Sessionize events with grouping, pairwise gaps, and bounded recent state."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import groupby, pairwise


@dataclass(frozen=True, slots=True)
class Event:
    user_id: str
    occurred_at: datetime
    action: str


def sessionize(events: list[Event], *, max_gap: timedelta) -> dict[str, list[list[str]]]:
    """Return action sessions per user in deterministic user/time order."""
    ordered = sorted(events, key=lambda event: (event.user_id, event.occurred_at))
    sessions: dict[str, list[list[str]]] = defaultdict(list)

    for user_id, user_events_iterator in groupby(ordered, key=lambda event: event.user_id):
        user_events = list(user_events_iterator)
        starts = {0}
        for index, (previous, current) in enumerate(pairwise(user_events), start=1):
            if current.occurred_at - previous.occurred_at > max_gap:
                starts.add(index)

        current_session: list[str] = []
        for index, event in enumerate(user_events):
            if index in starts and current_session:
                sessions[user_id].append(current_session)
                current_session = []
            current_session.append(event.action)
        if current_session:
            sessions[user_id].append(current_session)

    return dict(sessions)


def main() -> None:
    base = datetime.fromisoformat("2026-08-04T09:00:00+00:00")
    events = [
        Event("u2", base, "view"),
        Event("u1", base, "view"),
        Event("u1", base + timedelta(minutes=5), "click"),
        Event("u1", base + timedelta(minutes=45), "buy"),
        Event("u2", base + timedelta(minutes=2), "search"),
    ]
    sessions = sessionize(events, max_gap=timedelta(minutes=30))
    recent_u1 = deque((event.action for event in events if event.user_id == "u1"), maxlen=2)
    print(f"sessions={sessions}")
    print(f"bounded recent u1 actions={list(recent_u1)}")


if __name__ == "__main__":
    main()
