"""Functions, arguments, control flow, loops, and expected errors."""

from learn_python_quick.foundations import (
    JobStatus,
    batched,
    format_metric,
    next_action,
    safe_divide,
)


def main() -> None:
    for batch in batched(range(7), 3):
        print(f"batch={batch}")
    print(format_metric("success rate", safe_divide(9, 10), digits=1))
    for status in JobStatus:
        print(f"{status.value:>9} -> {next_action(status)}")

    try:
        list(batched([1, 2], 0))
    except ValueError as error:
        print(f"expected error: {error}")


if __name__ == "__main__":
    main()
