"""Call the optional prediction API in process; no port is opened."""

from fastapi.testclient import TestClient

from learn_python_quick.api import create_app


def main() -> None:
    client = TestClient(create_app())
    health = client.get("/health")
    prediction = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    print(f"health={health.status_code} {health.json()}")
    print(f"prediction={prediction.status_code} {prediction.json()}")


if __name__ == "__main__":
    main()
