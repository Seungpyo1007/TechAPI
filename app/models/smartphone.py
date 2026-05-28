"""Smartphone model (§6.4)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Smartphone(SQLModel, table=True):
    """A smartphone model (e.g. Galaxy S25)."""

    __tablename__ = "smartphones"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    name: str
    brand_id: int = Field(foreign_key="brands.id", index=True)
    soc_id: int = Field(foreign_key="socs.id", index=True)

    release_date: date
    msrp_usd: int | None = None

    # Memory
    ram_gb: int
    storage_options_gb: list[int] = Field(default_factory=list, sa_column=Column(JSON))

    # Display — {size_inch, resolution, refresh_hz, type, brightness_nits, ppi}
    display: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Cameras — [{type, mp, aperture, ois, sensor, ...}]
    cameras: list[dict[str, Any]] = Field(default_factory=list, sa_column=Column(JSON))

    # Battery
    battery_mah: int
    charging_wired_w: int | None = None
    charging_wireless_w: int | None = None

    # Physical
    weight_g: float
    dimensions: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    ip_rating: str | None = None

    # Software
    os: str
    os_version: str | None = None

    # Connectivity — {wifi, bluetooth, nfc, usb}
    connectivity: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Assets
    image_url: str | None = None
    images: list[str] = Field(default_factory=list, sa_column=Column(JSON))

    # Meta
    verified: bool = False
    source_urls: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
