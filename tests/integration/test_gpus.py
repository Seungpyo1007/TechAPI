"""Integration tests for discrete GPU endpoints (§7.2, ADR-011)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_gpus(client: TestClient) -> None:
    body = client.get("/v1/gpus?limit=100").json()
    assert body["count"] >= 40
    assert body["results"][0]["url"].startswith("/v1/gpus/")


def test_gpu_detail_embeds_manufacturer(client: TestClient) -> None:
    body = client.get("/v1/gpus/geforce-rtx-4090").json()
    assert body["slug"] == "geforce-rtx-4090"
    assert body["manufacturer"]["slug"] == "nvidia"
    assert body["manufacturer"]["url"] == "/v1/brands/nvidia"
    assert body["memory_gb"] >= 1
    assert body["cuda_cores"] is not None


def test_amd_gpu_uses_stream_processors(client: TestClient) -> None:
    body = client.get("/v1/gpus/radeon-rx-7900-xtx").json()
    assert body["manufacturer"]["slug"] == "amd"
    assert body["stream_processors"] is not None


def test_gpu_does_not_expose_proprietary_timespy(client: TestClient) -> None:
    # ADR-006: proprietary benchmark scores are not surfaced.
    body = client.get("/v1/gpus/geforce-rtx-4090").json()
    assert "timespy_score" not in body
    assert "blender_score" in body  # open-licensed score is allowed


def test_unknown_gpu_404(client: TestClient) -> None:
    response = client.get("/v1/gpus/nope")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
