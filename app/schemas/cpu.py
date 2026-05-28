"""Computer CPU response schema (§6.7).

Raw benchmark numbers (Cinebench/Geekbench) are algorithm inputs only and are not
exposed here (ADR-006).
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.common import ManufacturerRef


class CPURead(BaseModel):
    """Full CPU detail response."""

    id: int
    slug: str
    name: str
    manufacturer: ManufacturerRef
    release_date: date
    segment: str
    architecture: str
    socket: str | None = None
    process_node: str | None = None
    cores: int
    threads: int
    p_cores: int | None = None
    e_cores: int | None = None
    base_clock_ghz: float | None = None
    boost_clock_ghz: float | None = None
    l3_cache_mb: float | None = None
    tdp_w: int | None = None
    max_tdp_w: int | None = None
    integrated_graphics: str | None = None
    memory_support: str | None = None
    msrp_usd: int | None = None
    verified: bool
    source_urls: list[str]
    created_at: datetime
    updated_at: datetime
    url: str
