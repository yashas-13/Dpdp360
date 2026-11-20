from fastapi.testclient import TestClient

from app.main import create_app


def test_liveness_endpoint_returns_healthy_status() -> None:
    client = TestClient(create_app())

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
