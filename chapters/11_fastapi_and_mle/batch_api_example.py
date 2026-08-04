"""Exercise the bounded batch API in process without opening a port."""

from fastapi.testclient import TestClient

from learn_python_quick.api import create_app


def main() -> None:
    client = TestClient(create_app())
    rows = [
        {"features": [5.1, 3.5, 1.4, 0.2]},
        {"features": [6.0, 2.9, 4.5, 1.5]},
    ]
    response = client.post("/predict-batch", json={"rows": rows})
    labels = [prediction["label"] for prediction in response.json()["predictions"]]
    print(f"batch status={response.status_code} rows={len(labels)} labels={labels}")

    invalid = client.post("/predict-batch", json={"rows": []})
    print(f"empty batch status={invalid.status_code}")


if __name__ == "__main__":
    main()
