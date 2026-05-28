"""SoC response schemas (§6.3).

Note: raw benchmark numbers (Geekbench/AnTuTu) are intentionally **not** exposed
here — they are algorithm inputs only (ADR-006).
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel


class SoCManufacturer(BaseModel):
    """Manufacturer reference nested inside an embedded SoC (appendix C)."""

    slug: str
    name: str
    url: str


class SoCSummary(BaseModel):
    """SoC reference embedded in a smartphone detail (appendix C)."""

    id: int
    slug: str
    name: str
    manufacturer: SoCManufacturer
    process_nm: float
    gpu_name: str
    url: str


class SoCRead(BaseModel):
    """Full SoC detail response."""

    id: int
    slug: str
    name: str
    manufacturer: SoCManufacturer
    release_date: date
    process_nm: float
    transistors_billion: float | None = None
    cpu_config: dict[str, Any]
    gpu_name: str
    gpu_cores: int | None = None
    gpu_clock_mhz: int | None = None
    npu_tops: float | None = None
    modem: str | None = None
    verified: bool
    source_urls: list[str]
    created_at: datetime
    updated_at: datetime
    url: str
