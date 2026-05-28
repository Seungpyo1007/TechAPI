"""Integration tests for health/version and docs (§0.5.5, §15.1)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_health_sets_request_id_header(client: TestClient) -> None:
    response = client.get("/v1/health")
    assert response.headers["X-Request-ID"].startswith("req_")


def test_version_reports_algorithm(client: TestClient) -> None:
    body = client.get("/v1/version").json()
    assert body["api_version"] == "v1"
    assert body["scoring_algorithm_version"] == "1.0.0"


def test_openapi_schema_available(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 200


def test_scalar_docs_available(client: TestClient) -> None:
    response = client.get("/scalar")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_root_points_to_docs_and_health(client: TestClient) -> None:
    body = client.get("/").json()
    assert body["health"] == "/v1/health"
