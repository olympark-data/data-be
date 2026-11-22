from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["data"] == {"status": "ok"}


def test_health_db():
    res = client.get("/api/health/db")
    assert res.status_code == 200
    assert res.json()["data"]["db"] == "ok"


def test_swagger_disabled():
    for path in ["/docs", "/redoc", "/openapi.json", "/api/docs", "/api/openapi.json"]:
        assert client.get(path).status_code == 404
