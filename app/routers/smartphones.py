"""Smartphone endpoints (§7.2)."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Query
from sqlalchemy import func
from sqlmodel import Session, select
from sqlmodel.sql.expression import SelectOfScalar

from app.dependencies import PaginationDep, SessionDep
from app.errors import APIError, not_found
from app.models.brand import Brand
from app.models.smartphone import Smartphone
from app.models.soc import SoC
from app.routers.utils import build_ref_page
from app.schemas.common import Page, ResourceRef
from app.schemas.serializers import resource_ref, smartphone_read
from app.schemas.smartphone import ScoreRead, SmartphoneRead
from app.services.scoring import compute_scores

router = APIRouter(prefix="/smartphones", tags=["smartphones"])

# Allowlisted sort fields (§7.3) — guards against arbitrary column injection.
_SORT_FIELDS: dict[str, Any] = {
    "name": Smartphone.name,
    "release_date": Smartphone.release_date,
    "msrp_usd": Smartphone.msrp_usd,
}


def _apply_sort(stmt: SelectOfScalar[Smartphone], sort: str | None) -> SelectOfScalar[Smartphone]:
    if not sort:
        return stmt.order_by(Smartphone.name)
    descending = sort.startswith("-")
    field = sort[1:] if descending else sort
    column = _SORT_FIELDS.get(field)
    if column is None:
        raise APIError(400, "INVALID_REQUEST", f"Cannot sort by '{field}'")
    return stmt.order_by(column.desc() if descending else column.asc())


def _resolve_id(session: Session, model: Any, slug: str | None) -> int | None | str:
    """Return the id for a slug, ``None`` if no filter, or a sentinel when unmatched."""
    if slug is None:
        return None
    row = session.exec(select(model).where(model.slug == slug)).first()
    return row.id if row is not None else "MISSING"


@router.get("", summary="List smartphones")
def list_smartphones(
    session: SessionDep,
    pagination: PaginationDep,
    brand: Annotated[str | None, Query()] = None,
    soc: Annotated[str | None, Query()] = None,
    sort: Annotated[str | None, Query()] = None,
) -> Page[ResourceRef]:
    filters = []
    brand_id = _resolve_id(session, Brand, brand)
    soc_id = _resolve_id(session, SoC, soc)

    # An explicitly requested but unknown brand/soc yields an empty (not errored) page.
    if brand_id == "MISSING" or soc_id == "MISSING":
        return build_ref_page([], count=0, path="/v1/smartphones", pagination=pagination)

    if brand_id is not None:
        filters.append(Smartphone.brand_id == brand_id)
    if soc_id is not None:
        filters.append(Smartphone.soc_id == soc_id)

    count_stmt = select(func.count()).select_from(Smartphone)
    list_stmt = select(Smartphone)
    for clause in filters:
        count_stmt = count_stmt.where(clause)
        list_stmt = list_stmt.where(clause)

    count = session.exec(count_stmt).one()
    list_stmt = _apply_sort(list_stmt, sort).offset(pagination.offset).limit(pagination.limit)
    rows = session.exec(list_stmt).all()

    refs = [resource_ref("smartphones", p.slug, p.name) for p in rows]
    applied = {k: v for k, v in (("brand", brand), ("soc", soc), ("sort", sort)) if v}
    return build_ref_page(
        refs, count=count, path="/v1/smartphones", pagination=pagination, filters=applied
    )


def _load_full(session: SessionDep, slug: str) -> tuple[Smartphone, Brand, SoC, Brand]:
    phone = session.exec(select(Smartphone).where(Smartphone.slug == slug)).first()
    if phone is None:
        raise not_found("Smartphone", slug)
    brand = session.get(Brand, phone.brand_id)
    soc = session.get(SoC, phone.soc_id)
    if brand is None or soc is None:  # pragma: no cover - guarded by FK + validation
        raise not_found("Smartphone", slug)
    soc_manufacturer = session.get(Brand, soc.manufacturer_id)
    if soc_manufacturer is None:  # pragma: no cover
        raise not_found("Brand", str(soc.manufacturer_id))
    return phone, brand, soc, soc_manufacturer


@router.get("/{slug}", summary="Get a smartphone")
def get_smartphone(slug: str, session: SessionDep) -> SmartphoneRead:
    phone, brand, soc, soc_manufacturer = _load_full(session, slug)
    scores = compute_scores(phone, soc)
    return smartphone_read(phone, brand, soc, soc_manufacturer, scores)


@router.get("/{slug}/score", summary="Get a smartphone's scores")
def get_smartphone_score(slug: str, session: SessionDep) -> ScoreRead:
    phone, _brand, soc, _manufacturer = _load_full(session, slug)
    scores = compute_scores(phone, soc)
    return ScoreRead(
        algorithm_version=scores.algorithm_version,
        overall=scores.overall,
        performance=scores.performance,
        camera=scores.camera,
        battery=scores.battery,
        display=scores.display,
        value=scores.value,
    )
