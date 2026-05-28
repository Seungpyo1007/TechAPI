"""Discrete GPU model (§6.5). Defined for schema completeness; endpoints land in Phase 1 (P1)."""

from __future__ import annotations

from datetime import date

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class DiscreteGPU(SQLModel, table=True):
    """A discrete graphics card (e.g. GeForce RTX 5090)."""

    __tablename__ = "gpus"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    name: str
    manufacturer_id: int = Field(foreign_key="brands.id", index=True)
    architecture: str
    release_date: date
    msrp_usd: int | None = None

    # Cores
    cuda_cores: int | None = None
    stream_processors: int | None = None
    rt_cores: int | None = None
    tensor_cores: int | None = None

    # Memory
    memory_gb: int
    memory_type: str
    memory_bus_bit: int
    memory_bandwidth_gbps: float | None = None

    # Clock
    base_clock_mhz: int
    boost_clock_mhz: int

    # Power
    tdp_w: int
    pcie_version: str

    # Benchmarks (open licenses only)
    blender_score: float | None = None
    timespy_score: int | None = None

    # Meta
    verified: bool = False
    source_urls: list[str] = Field(default_factory=list, sa_column=Column(JSON))
