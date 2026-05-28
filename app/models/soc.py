"""SoC model (§6.3)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class SoC(SQLModel, table=True):
    """A System-on-Chip (e.g. Snapdragon 8 Elite)."""

    __tablename__ = "socs"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    name: str
    manufacturer_id: int = Field(foreign_key="brands.id", index=True)
    release_date: date
    process_nm: float
    transistors_billion: float | None = None

    # CPU — JSONB: {"performance": 2, "efficiency": 6, "clocks": [...]}
    cpu_config: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Integrated GPU
    gpu_name: str
    gpu_cores: int | None = None
    gpu_clock_mhz: int | None = None

    # AI
    npu_tops: float | None = None

    # Modem
    modem: str | None = None

    # Benchmarks (raw, algorithm input only — never re-exposed, ADR-006)
    geekbench_single: int | None = None
    geekbench_multi: int | None = None
    antutu_score: int | None = None

    # Meta
    verified: bool = False
    source_urls: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
