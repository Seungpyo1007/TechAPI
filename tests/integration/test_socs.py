"""Integration tests for SoC endpoints (§7.2)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_list_socs(client: TestClient) -> None:
    body = client.get("/v1/socs").json()
    assert body["count"] >= 5  # §0.5.5: socs 5+


def test_get_soc_detail_embeds_manufacturer(client: TestClient) -> None:
    body = client.get("/v1/socs/snapdragon-8-elite").json()
    assert body["slug"] == "snapdragon-8-elite"
    assert body["manufacturer"]["slug"] == "qualcomm"
    assert body["manufacturer"]["url"] == "/v1/brands/qualcomm"
    assert body["process_nm"] == 3.0
    assert body["gpu_name"] == "Adreno 830"


def test_soc_detail_does_not_expose_raw_benchmarks(client: TestClient) -> None:
    # ADR-006: Geekbench/AnTuTu numbers are algorithm inputs only.
    body = client.get("/v1/socs/snapdragon-8-elite").json()
    assert "geekbench_single" not in body
    assert "antutu_score" not in body


def test_unknown_soc_404(client: TestClient) -> None:
    assert client.get("/v1/socs/nope").status_code == 404


def test_soc_smartphones_relation(client: TestClient) -> None:
    body = client.get("/v1/socs/snapdragon-8-elite/smartphones").json()
    slugs = {item["slug"] for item in body["results"]}
    assert {"galaxy-s25", "oneplus-13"} <= slugs
