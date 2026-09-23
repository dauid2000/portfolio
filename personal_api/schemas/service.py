"""Pydantic schemas for services."""
from pydantic import BaseModel, ConfigDict, Field


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str = Field(min_length=2, max_length=160)
    description: str
