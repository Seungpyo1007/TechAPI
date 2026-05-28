"""Brand endpoints (§7.2)."""

from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import func
from sqlmodel import select

from app.dependencies import PaginationDep, SessionDep
from app.errors import not_found
from app.models.brand import Brand
from app.models.smartphone import Smartphone
from app.routers.utils import build_ref_page
from app.schemas.brand import BrandRead
from app.schemas.common import Page, ResourceRef
from app.schemas.serializers import brand_read, resource_ref

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get("", summary="List brands")
def list_brands(session: SessionDep, pagination: PaginationDep) -> Page[ResourceRef]:
    count = session.exec(select(func.count()).select_from(Brand)).one()
    rows = session.exec(
        select(Brand).order_by(Brand.name).offset(pagination.offset).limit(pagination.limit)
    ).all()
    refs = [resource_ref("brands", b.slug, b.name) for b in rows]
    return build_ref_page(refs, count=count, path="/v1/brands", pagination=pagination)


@router.get("/{slug}", summary="Get a brand")
def get_brand(slug: str, session: SessionDep) -> BrandRead:
    brand = session.exec(select(Brand).where(Brand.slug == slug)).first()
    if brand is None:
        raise not_found("Brand", slug)
    return brand_read(brand)


@router.get("/{slug}/smartphones", summary="Smartphones by this brand")
def brand_smartphones(
    slug: str, session: SessionDep, pagination: PaginationDep
) -> Page[ResourceRef]:
    brand = session.exec(select(Brand).where(Brand.slug == slug)).first()
    if brand is None:
        raise not_found("Brand", slug)

    count = session.exec(
        select(func.count()).select_from(Smartphone).where(Smartphone.brand_id == brand.id)
    ).one()
    rows = session.exec(
        select(Smartphone)
        .where(Smartphone.brand_id == brand.id)
        .order_by(Smartphone.name)
        .offset(pagination.offset)
        .limit(pagination.limit)
    ).all()
    refs = [resource_ref("smartphones", p.slug, p.name) for p in rows]
    return build_ref_page(
        refs, count=count, path=f"/v1/brands/{slug}/smartphones", pagination=pagination
    )
