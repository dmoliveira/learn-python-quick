"""Benchmark an algorithmic data-structure choice without a speed assertion."""

from statistics import median
from timeit import repeat


def count_matches(values: list[int], candidates: list[int] | set[int]) -> int:
    return sum(value in candidates for value in values)


def main() -> None:
    values = list(range(2_000, 4_000))
    candidate_list = list(range(3_000))
    candidate_set = set(candidate_list)
    assert count_matches(values, candidate_list) == count_matches(values, candidate_set)

    list_runs = repeat(lambda: count_matches(values, candidate_list), repeat=3, number=2)
    set_runs = repeat(lambda: count_matches(values, candidate_set), repeat=3, number=2)
    print(f"same matches={count_matches(values, candidate_list)}")
    print(f"median list={median(list_runs):.6f}s set={median(set_runs):.6f}s")


if __name__ == "__main__":
    main()
