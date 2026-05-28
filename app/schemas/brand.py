"""Brand response schemas (§6.2)."""

from __future__ import annotations

from pydantic import BaseModel


class BrandSummary(BaseModel):
    """Brand reference embedded in other resources (appendix C)."""

    id: int
    slug: str
    name: str
    country: str | None = None
    url: str


class BrandRead(BaseModel):
    """Full brand detail response."""

    id: int
    slug: str
    name: str
    country: str | None = None
    founded_year: int | None = None
    logo_url: str | None = None
    website: str | None = None
    description_en: str | None = None
    description_ko: str | None = None
    url: str
