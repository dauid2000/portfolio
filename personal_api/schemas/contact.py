"""Contact form input/output schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    subject: str | None = Field(default=None, max_length=200)
    message: str = Field(min_length=10, max_length=5000)


class ContactOut(ContactCreate):
    """Admin-facing representation — never returned by public endpoints."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    is_read: bool
