"""Standard data structures, collections, and itertools."""

from collections import Counter, deque
from itertools import pairwise

from learn_python_quick.foundations import batched


def main() -> None:
    events = ["view", "view", "click", "view", "buy", "click"]
    counts = Counter(events)
    recent = deque(events, maxlen=3)
    ordered = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))

    print(f"counts={dict(ordered)}")
    print(f"recent={list(recent)}")
    print(f"unique={set(events)}")
    print(f"pairs={list(pairwise([3, 5, 8, 13]))}")
    print(f"lazy batches={list(batched((value * value for value in range(5)), 2))}")


if __name__ == "__main__":
    main()
