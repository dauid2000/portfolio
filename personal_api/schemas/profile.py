"""Pydantic schemas for the profile endpoint."""
from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    profession: str
    university: str
    email: EmailStr
    phone: str
    alt_phone: str | None = None
    location: str | None = None
    bio: str | None = None
