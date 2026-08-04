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
