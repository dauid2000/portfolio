"""Pydantic schemas for education records."""
from pydantic import BaseModel, ConfigDict, Field


class EducationBase(BaseModel):
    institution: str = Field(min_length=2, max_length=200)
    programme: str = Field(min_length=2, max_length=200)
    level: str = Field(min_length=2, max_length=80)
    status: str = Field(default="Currently Studying", max_length=80)


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: str | None = Field(default=None, min_length=2, max_length=200)
    programme: str | None = Field(default=None, min_length=2, max_length=200)
    level: str | None = Field(default=None, min_length=2, max_length=80)
    status: str | None = Field(default=None, max_length=80)


class EducationOut(EducationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
