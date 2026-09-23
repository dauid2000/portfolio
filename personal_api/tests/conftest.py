"""Shared pytest fixtures.

A dedicated test database is used (set via environment variables BEFORE
the app modules are imported), and it is seeded once per test session.
"""
import os

os.environ["DATABASE_URL"] = "sqlite:///./data/test_api.db"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "TestAdmin-2026"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from database import Base, SessionLocal, engine  # noqa: E402
from init_db import seed_initial_data  # noqa: E402
from main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables, seed once, then drop everything after the session."""
    Base.metadata.create_all(bind=engine)
    seed_initial_data()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def admin_headers(client):
    """Login once and reuse the token for all admin-only tests."""
    res = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "TestAdmin-2026"},
    )
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
