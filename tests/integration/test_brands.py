"""Integration tests for brand endpoints (§7.2)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_brands_pagination_envelope(client: TestClient) -> None:
    body = client.get("/v1/brands").json()
    assert body["count"] >= 5  # §0.5.5: brands 5+
    assert set(body.keys()) == {"count", "next", "previous", "results"}
    assert {"slug", "name", "url"} <= body["results"][0].keys()


def test_get_brand_detail(client: TestClient) -> None:
    body = client.get("/v1/brands/samsung").json()
    assert body["slug"] == "samsung"
    assert body["country"] == "KR"
    assert body["url"] == "/v1/brands/samsung"


def test_unknown_brand_returns_404_envelope(client: TestClient) -> None:
    response = client.get("/v1/brands/does-not-exist")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "NOT_FOUND"
    assert "does-not-exist" in error["message"]
    assert error["request_id"].startswith("req_")


def test_brand_smartphones_relation(client: TestClient) -> None:
    body = client.get("/v1/brands/samsung/smartphones?limit=100").json()
    assert body["count"] >= 1
    slugs = {item["slug"] for item in body["results"]}
    assert "galaxy-s25" in slugs


def test_brand_smartphones_unknown_brand_404(client: TestClient) -> None:
    assert client.get("/v1/brands/nope/smartphones").status_code == 404


def test_brands_pagination_limit(client: TestClient) -> None:
    body = client.get("/v1/brands?limit=2").json()
    assert len(body["results"]) == 2
    assert body["next"] is not None
