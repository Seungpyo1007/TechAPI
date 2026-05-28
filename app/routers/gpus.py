"""Discrete GPU endpoints (§7.2)."""

from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import func
from sqlmodel import select

from app.dependencies import PaginationDep, SessionDep
from app.errors import not_found
from app.models.brand import Brand
from app.models.gpu import DiscreteGPU
from app.routers.utils import build_ref_page
from app.schemas.common import Page, ResourceRef
from app.schemas.gpu import GPURead
from app.schemas.serializers import gpu_read, resource_ref

router = APIRouter(prefix="/gpus", tags=["gpus"])


@router.get("", summary="List discrete GPUs")
def list_gpus(session: SessionDep, pagination: PaginationDep) -> Page[ResourceRef]:
    count = session.exec(select(func.count()).select_from(DiscreteGPU)).one()
    rows = session.exec(
        select(DiscreteGPU)
        .order_by(DiscreteGPU.name)
        .offset(pagination.offset)
        .limit(pagination.limit)
    ).all()
    refs = [resource_ref("gpus", g.slug, g.name) for g in rows]
    return build_ref_page(refs, count=count, path="/v1/gpus", pagination=pagination)


@router.get("/{slug}", summary="Get a discrete GPU")
def get_gpu(slug: str, session: SessionDep) -> GPURead:
    gpu = session.exec(select(DiscreteGPU).where(DiscreteGPU.slug == slug)).first()
    if gpu is None:
        raise not_found("GPU", slug)
    manufacturer = session.get(Brand, gpu.manufacturer_id)
    if manufacturer is None:  # pragma: no cover - guarded by FK + validation
        raise not_found("Brand", str(gpu.manufacturer_id))
    return gpu_read(gpu, manufacturer)
