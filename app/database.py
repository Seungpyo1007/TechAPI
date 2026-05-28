"""Database engine and session management (§4.3 SQLModel layer)."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, create_engine

# Import models so SQLModel.metadata is fully populated before create_all.
from app import models  # noqa: F401,E402  (side-effect import)
from app.config import settings


def _build_engine() -> Engine:
    url = settings.database_url
    connect_args: dict[str, object] = {}
    engine_kwargs: dict[str, object] = {}
    if url.startswith("sqlite"):
        # Needed for FastAPI + SQLite when sharing a connection across threads.
        connect_args["check_same_thread"] = False
    else:
        engine_kwargs["pool_size"] = settings.database_pool_size
        engine_kwargs["pool_pre_ping"] = True
    return create_engine(url, connect_args=connect_args, **engine_kwargs)


engine: Engine = _build_engine()


def create_db_and_tables() -> None:
    """Create all tables. Phase 0 helper; Phase 1+ uses Alembic migrations."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session."""
    with Session(engine) as session:
        yield session
