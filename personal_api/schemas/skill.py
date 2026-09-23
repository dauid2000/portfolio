"""Pydantic schemas for skills."""
from pydantic import BaseModel, ConfigDict, Field


class SkillBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(default="General", max_length=80)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    category: str | None = Field(default=None, max_length=80)


class SkillOut(SkillBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
