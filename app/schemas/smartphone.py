"""Smartphone response schemas (§6.4, appendix C)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.brand import BrandSummary
from app.schemas.soc import SoCSummary


class ScoreRead(BaseModel):
    """Computed scores (§8)."""

    algorithm_version: str
    overall: float | None = None
    performance: float | None = None
    camera: float | None = None
    battery: float | None = None
    display: float | None = None
    value: float | None = None


class SmartphoneRead(BaseModel):
    """Full smartphone detail response (appendix C)."""

    id: int
    slug: str
    name: str
    brand: BrandSummary
    soc: SoCSummary
    release_date: date
    msrp_usd: int | None = None
    ram_gb: int
    storage_options_gb: list[int]
    display: dict[str, Any]
    cameras: list[dict[str, Any]]
    battery_mah: int
    charging_wired_w: int | None = None
    charging_wireless_w: int | None = None
    weight_g: float
    dimensions: dict[str, Any]
    ip_rating: str | None = None
    os: str
    os_version: str | None = None
    connectivity: dict[str, Any]
    image_url: str | None = None
    images: list[str] = []
    score: ScoreRead
    verified: bool
    source_urls: list[str]
    created_at: datetime
    updated_at: datetime
