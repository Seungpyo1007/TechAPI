"""Shared pytest fixtures.

Tests run against a throwaway SQLite database seeded from ``data/``. The env var
is set *before* importing the app so config/engine pick it up (§15.2).
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator
from pathlib import Path

_TMP_DIR = tempfile.mkdtemp(prefix="techapi-test-")
_DB_PATH = Path(_TMP_DIR) / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_PATH}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _seeded_database() -> Iterator[None]:
    from app.database import create_db_and_tables, engine
    from scripts.seed import seed

    create_db_and_tables()
    with Session(engine) as session:
        seed(session)
    yield


@pytest.fixture
def client() -> Iterator[TestClient]:
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
