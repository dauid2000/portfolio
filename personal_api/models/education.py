"""Education model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution: Mapped[str] = mapped_column(String(200))
    programme: Mapped[str] = mapped_column(String(200))
    level: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(80), default="Currently Studying")
