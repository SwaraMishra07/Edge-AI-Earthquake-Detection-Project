from fastapi.testclient import TestClient
from app.api import app


def test_root_status():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"
