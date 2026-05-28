"""Brand model (§6.2)."""

from __future__ import annotations

from sqlmodel import Field, SQLModel


class Brand(SQLModel, table=True):
    """A manufacturer of devices and/or SoCs (e.g. Samsung, Qualcomm)."""

    __tablename__ = "brands"

    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    name: str
    country: str | None = None  # ISO 3166 alpha-2, e.g. "KR"
    founded_year: int | None = None
    logo_url: str | None = None
    website: str | None = None
    description_en: str | None = None
    description_ko: str | None = None
