import pytest
from fastapi.testclient import TestClient

from learn_python_quick.api import create_app

pytestmark = pytest.mark.api


def test_prediction_api_in_process() -> None:
    client = TestClient(create_app())
    assert client.get("/health").json() == {
        "status": "ok",
        "model_version": "iris-logistic-v1",
    }
    response = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    assert response.json()["label"] == "setosa"
    assert 0 <= response.json()["confidence"] <= 1


def test_prediction_api_rejects_wrong_shape_and_extra_fields() -> None:
    client = TestClient(create_app())
    assert client.post("/predict", json={"features": [1, 2, 3]}).status_code == 422
    assert (
        client.post(
            "/predict",
            json={"features": [5.1, 3.5, 1.4, 0.2], "secret": "no"},
        ).status_code
        == 422
    )


def test_batch_prediction_is_bounded_and_preserves_row_order() -> None:
    client = TestClient(create_app())
    rows = [
        {"features": [5.1, 3.5, 1.4, 0.2]},
        {"features": [6.0, 2.9, 4.5, 1.5]},
    ]
    response = client.post("/predict-batch", json={"rows": rows})
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert [prediction["label"] for prediction in predictions] == ["setosa", "versicolor"]
    assert {prediction["model_version"] for prediction in predictions} == {"iris-logistic-v1"}

    assert client.post("/predict-batch", json={"rows": []}).status_code == 422
    assert client.post("/predict-batch", json={"rows": rows * 51}).status_code == 422
    assert (
        client.post(
            "/predict-batch",
            json={"rows": [{**rows[0], "unexpected": True}]},
        ).status_code
        == 422
    )
