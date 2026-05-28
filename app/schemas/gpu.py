"""Discrete GPU response schema (§6.5).

Proprietary benchmark numbers (e.g. 3DMark Time Spy) are not exposed; only the
open-licensed Blender Open Data score is surfaced (ADR-006, §8.5).
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from app.schemas.common import ManufacturerRef


class GPURead(BaseModel):
    """Full discrete GPU detail response."""

    id: int
    slug: str
    name: str
    manufacturer: ManufacturerRef
    architecture: str
    release_date: date
    msrp_usd: int | None = None
    cuda_cores: int | None = None
    stream_processors: int | None = None
    rt_cores: int | None = None
    tensor_cores: int | None = None
    memory_gb: float
    memory_type: str
    memory_bus_bit: int
    memory_bandwidth_gbps: float | None = None
    base_clock_mhz: int
    boost_clock_mhz: int
    tdp_w: int
    pcie_version: str
    blender_score: float | None = None
    verified: bool
    source_urls: list[str]
    url: str
