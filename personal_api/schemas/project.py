"""Pydantic schemas for projects."""
from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    description: str = Field(min_length=10)
    tagline: str | None = Field(default=None, max_length=200)
    technologies: list[str] = Field(default_factory=list)
    project_url: str | None = Field(default=None, max_length=300)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    """All fields optional — send only what you want to change."""
    name: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, min_length=10)
    tagline: str | None = Field(default=None, max_length=200)
    technologies: list[str] | None = None
    project_url: str | None = Field(default=None, max_length=300)


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: str
