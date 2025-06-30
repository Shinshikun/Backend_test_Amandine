from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

class LabelBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    color: str

class LabelCreate(BaseModel):
    title: str
    color: str

class LabelResponse(LabelBase):
    pass

class LabelUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Optional[str] = None
    color: Optional[str] = None
