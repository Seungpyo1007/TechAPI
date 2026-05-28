"""Shared response envelopes (§7.4 list, §7.5 error)."""

from __future__ import annotations

from pydantic import BaseModel


class ResourceRef(BaseModel):
    """A lightweight reference used in list responses (§7.4)."""

    slug: str
    name: str
    url: str


class ManufacturerRef(BaseModel):
    """A manufacturer (brand) reference embedded in a component detail."""

    slug: str
    name: str
    url: str


class Page[T](BaseModel):
    """Paginated collection envelope (§7.4)."""

    count: int
    next: str | None = None
    previous: str | None = None
    results: list[T]


class ErrorBody(BaseModel):
    """Error detail (§7.5)."""

    code: str
    message: str
    request_id: str
    documentation_url: str | None = None


class ErrorResponse(BaseModel):
    """Top-level error envelope (§7.5)."""

    error: ErrorBody
