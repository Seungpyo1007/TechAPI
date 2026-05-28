"""Tests for the static dump generator (§4.2, §16.1)."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from scripts.dump import generate


def test_dump_writes_list_detail_and_manifest(client: TestClient, tmp_path: Path) -> None:
    counts = generate(client, output_dir=tmp_path)
    assert counts["smartphones"] >= 10
    assert counts["gpus"] >= 1
    assert counts["cpus"] >= 1

    # Detail file matches the live API response.
    detail_file = tmp_path / "v1" / "smartphones" / "galaxy-s25" / "index.json"
    assert detail_file.exists()
    detail = json.loads(detail_file.read_text())
    assert detail["slug"] == "galaxy-s25"
    assert detail == client.get("/v1/smartphones/galaxy-s25").json()

    # Score sidecar is dumped for smartphones.
    assert (tmp_path / "v1" / "smartphones" / "galaxy-s25" / "score" / "index.json").exists()

    # Combined list file holds every item.
    listing = json.loads((tmp_path / "v1" / "smartphones" / "index.json").read_text())
    assert listing["count"] == len(listing["results"])

    # Manifest enumerates all collections.
    manifest = json.loads((tmp_path / "v1" / "index.json").read_text())
    assert {"brands", "socs", "smartphones", "gpus", "cpus"} <= manifest["collections"].keys()
