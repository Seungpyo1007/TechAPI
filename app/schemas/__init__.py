"""Pydantic response schemas (§7.4 list, appendix C detail, §7.5 error)."""

from app.schemas.brand import BrandRead, BrandSummary
from app.schemas.common import ErrorBody, ErrorResponse, Page, ResourceRef
from app.schemas.smartphone import ScoreRead, SmartphoneRead
from app.schemas.soc import SoCManufacturer, SoCRead, SoCSummary

__all__ = [
    "Page",
    "ResourceRef",
    "ErrorBody",
    "ErrorResponse",
    "BrandRead",
    "BrandSummary",
    "SoCRead",
    "SoCSummary",
    "SoCManufacturer",
    "SmartphoneRead",
    "ScoreRead",
]
