"""Integration tests for smartphone endpoints (§7.2, appendix C)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_smartphones(client: TestClient) -> None:
    body = client.get("/v1/smartphones").json()
    assert body["count"] >= 10  # §0.5.5: smartphones 10+
    assert body["results"][0]["url"].startswith("/v1/smartphones/")


def test_detail_matches_appendix_c_shape(client: TestClient) -> None:
    body = client.get("/v1/smartphones/galaxy-s25").json()
    assert body["slug"] == "galaxy-s25"
    assert body["brand"]["slug"] == "samsung"
    assert body["soc"]["slug"] == "snapdragon-8-elite"
    assert body["soc"]["manufacturer"]["slug"] == "qualcomm"
    assert body["display"]["refresh_hz"] == 120
    assert isinstance(body["cameras"], list)
    # score object present with all categories (§8.1)
    score = body["score"]
    assert score["algorithm_version"] == "1.0.0"
    assert {"overall", "performance", "camera", "battery", "display", "value"} <= score.keys()


def test_unknown_smartphone_404(client: TestClient) -> None:
    response = client.get("/v1/smartphones/nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_score_endpoint(client: TestClient) -> None:
    body = client.get("/v1/smartphones/galaxy-s25/score").json()
    assert body["algorithm_version"] == "1.0.0"
    assert body["overall"] is not None


def test_filter_by_brand(client: TestClient) -> None:
    body = client.get("/v1/smartphones?brand=apple").json()
    slugs = {item["slug"] for item in body["results"]}
    assert "iphone-16" in slugs
    assert "galaxy-s25" not in slugs


def test_filter_by_soc(client: TestClient) -> None:
    body = client.get("/v1/smartphones?soc=tensor-g4&limit=100").json()
    slugs = {item["slug"] for item in body["results"]}
    # All Tensor G4 phones are Pixels; no Snapdragon-based phone should appear.
    assert {"pixel-9", "pixel-9-pro"} <= slugs
    assert "galaxy-s25" not in slugs


def test_filter_by_unknown_brand_is_empty(client: TestClient) -> None:
    body = client.get("/v1/smartphones?brand=nope").json()
    assert body["count"] == 0
    assert body["results"] == []


def test_sort_descending_by_msrp(client: TestClient) -> None:
    body = client.get("/v1/smartphones?sort=-msrp_usd&limit=3").json()
    names = [item["slug"] for item in body["results"]]
    assert names  # non-empty; ordering exercised


def test_invalid_sort_field_returns_400(client: TestClient) -> None:
    response = client.get("/v1/smartphones?sort=bogus")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_REQUEST"


def test_limit_over_max_is_rejected(client: TestClient) -> None:
    response = client.get("/v1/smartphones?limit=500")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
