"""Operational endpoints: health and version (§7.2)."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["meta"])


@router.get("/health", summary="Health check")
def health() -> dict[str, str]:
    """Liveness probe used by the deploy pipeline (§16.3)."""
    return {"status": "ok", "version": settings.version}


@router.get("/version", summary="API and algorithm versions")
def version() -> dict[str, str]:
    """Report the API version and the scoring algorithm version (§7.7, §8.6)."""
    return {
        "api_version": "v1",
        "release": settings.version,
        "scoring_algorithm_version": settings.scoring_algorithm_version,
    }
