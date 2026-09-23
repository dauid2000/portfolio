"""Project model."""
from datetime import datetime, timezone

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    description: Mapped[str] = mapped_column(Text)
    tagline: Mapped[str | None] = mapped_column(String(200), nullable=True)
    technologies: Mapped[str] = mapped_column(String(400), default="")  # comma-separated
    project_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
    created_at: Mapped[str] = mapped_column(
        String(30),  # ISO timestamp
        default=lambda: datetime.now(timezone.utc).isoformat(),
    )
