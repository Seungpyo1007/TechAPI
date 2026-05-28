"""Pagination helpers for list endpoints (§7.4)."""

from __future__ import annotations

from app.config import settings
from app.dependencies import DEFAULT_LIMIT, Pagination
from app.schemas.common import Page, ResourceRef

PREFIX = settings.api_version_prefix


def _page_url(path: str, limit: int, offset: int, extra: dict[str, str]) -> str:
    params = dict(extra)
    params["offset"] = str(offset)
    if limit != DEFAULT_LIMIT:
        params["limit"] = str(limit)
    query = "&".join(f"{key}={value}" for key, value in params.items())
    return f"{path}?{query}"


def build_ref_page(
    refs: list[ResourceRef],
    *,
    count: int,
    path: str,
    pagination: Pagination,
    filters: dict[str, str] | None = None,
) -> Page[ResourceRef]:
    """Wrap reference items in the §7.4 paginated envelope with next/previous links."""
    extra = filters or {}
    limit, offset = pagination.limit, pagination.offset
    next_url = (
        _page_url(path, limit, offset + limit, extra) if offset + limit < count else None
    )
    previous_url = (
        _page_url(path, limit, max(offset - limit, 0), extra) if offset > 0 else None
    )
    return Page[ResourceRef](
        count=count, next=next_url, previous=previous_url, results=refs
    )
