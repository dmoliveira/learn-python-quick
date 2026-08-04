"""Parse a local log and exercise an HTTP boundary with a fake session."""

from pathlib import Path

from learn_python_quick.text_io import ResponseLike, fetch_json, incident_events


class FakeResponse(ResponseLike):
    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return {"service": "checkout", "healthy": True}


class FakeSession:
    def get(self, url: str, *, timeout: float) -> ResponseLike:
        print(f"fake GET {url} timeout={timeout}")
        return FakeResponse()


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    log_path = root / "datasets/generated/incidents.log"
    with log_path.open(encoding="utf-8") as stream:
        incidents, invalid_count = incident_events(iter(stream))
    print(f"incidents={len(incidents)} invalid={invalid_count}")
    print(fetch_json("https://example.invalid/health", session=FakeSession(), timeout=2.0))


if __name__ == "__main__":
    main()
