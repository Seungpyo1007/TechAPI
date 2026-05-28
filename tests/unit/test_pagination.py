"""Unit tests for pagination link building (§7.4)."""

from __future__ import annotations

from app.dependencies import Pagination
from app.routers.utils import build_ref_page
from app.schemas.common import ResourceRef


def _refs(n: int) -> list[ResourceRef]:
    return [ResourceRef(slug=f"s{i}", name=f"N{i}", url=f"/v1/x/s{i}") for i in range(n)]


def test_first_page_has_next_no_previous() -> None:
    page = build_ref_page(
        _refs(20), count=50, path="/v1/smartphones", pagination=Pagination(limit=20, offset=0)
    )
    assert page.previous is None
    assert page.next == "/v1/smartphones?offset=20"


def test_middle_page_has_both_links() -> None:
    page = build_ref_page(
        _refs(20), count=50, path="/v1/smartphones", pagination=Pagination(limit=20, offset=20)
    )
    assert page.previous == "/v1/smartphones?offset=0"
    assert page.next == "/v1/smartphones?offset=40"


def test_last_page_has_no_next() -> None:
    page = build_ref_page(
        _refs(10), count=50, path="/v1/smartphones", pagination=Pagination(limit=20, offset=40)
    )
    assert page.next is None
    assert page.previous == "/v1/smartphones?offset=20"


def test_filters_are_preserved_in_links() -> None:
    page = build_ref_page(
        _refs(20),
        count=50,
        path="/v1/smartphones",
        pagination=Pagination(limit=20, offset=0),
        filters={"brand": "samsung"},
    )
    assert page.next is not None
    assert "brand=samsung" in page.next


def test_non_default_limit_is_included() -> None:
    page = build_ref_page(
        _refs(5), count=50, path="/v1/smartphones", pagination=Pagination(limit=5, offset=0)
    )
    assert page.next is not None
    assert "limit=5" in page.next
