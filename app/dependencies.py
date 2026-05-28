"""Shared FastAPI dependencies (§5.3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Query
from sqlmodel import Session

from app.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

MAX_LIMIT = 100
DEFAULT_LIMIT = 20


@dataclass(slots=True)
class Pagination:
    """Offset/limit pagination parameters (§7.3)."""

    limit: int
    offset: int


def pagination_params(
    limit: Annotated[int, Query(ge=1, le=MAX_LIMIT)] = DEFAULT_LIMIT,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Pagination:
    """Parse and validate ``?limit`` / ``?offset`` (§7.3)."""
    return Pagination(limit=limit, offset=offset)


PaginationDep = Annotated[Pagination, Depends(pagination_params)]
