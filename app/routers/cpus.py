"""Computer CPU endpoints (§7.2, §6.7)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy import func
from sqlmodel import select

from app.dependencies import PaginationDep, SessionDep
from app.errors import not_found
from app.models.brand import Brand
from app.models.cpu import CPU
from app.routers.utils import build_ref_page
from app.schemas.common import Page, ResourceRef
from app.schemas.cpu import CPURead
from app.schemas.serializers import cpu_read, resource_ref

router = APIRouter(prefix="/cpus", tags=["cpus"])


@router.get("", summary="List CPUs")
def list_cpus(
    session: SessionDep,
    pagination: PaginationDep,
    segment: Annotated[str | None, Query()] = None,
) -> Page[ResourceRef]:
    count_stmt = select(func.count()).select_from(CPU)
    list_stmt = select(CPU)
    if segment is not None:
        count_stmt = count_stmt.where(CPU.segment == segment)
        list_stmt = list_stmt.where(CPU.segment == segment)

    count = session.exec(count_stmt).one()
    rows = session.exec(
        list_stmt.order_by(CPU.name).offset(pagination.offset).limit(pagination.limit)
    ).all()
    refs = [resource_ref("cpus", c.slug, c.name) for c in rows]
    filters = {"segment": segment} if segment else None
    return build_ref_page(
        refs, count=count, path="/v1/cpus", pagination=pagination, filters=filters
    )


@router.get("/{slug}", summary="Get a CPU")
def get_cpu(slug: str, session: SessionDep) -> CPURead:
    cpu = session.exec(select(CPU).where(CPU.slug == slug)).first()
    if cpu is None:
        raise not_found("CPU", slug)
    manufacturer = session.get(Brand, cpu.manufacturer_id)
    if manufacturer is None:  # pragma: no cover - guarded by FK + validation
        raise not_found("Brand", str(cpu.manufacturer_id))
    return cpu_read(cpu, manufacturer)
