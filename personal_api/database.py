"""Database layer: engine, session factory and declarative base.

Routes never touch this module directly — they receive a Session through
the get_db() dependency, which keeps DB handling separate from the API.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

# Make sure the data/ directory exists before SQLite opens the file
if settings.DATABASE_URL.startswith("sqlite"):
    db_path = settings.DATABASE_URL.split("///")[-1]
    directory = os.path.dirname(db_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    # check_same_thread=False is required only for SQLite with FastAPI
    connect_args={"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_db():
    """FastAPI dependency: one session per request, always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
