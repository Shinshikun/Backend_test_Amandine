from __future__ import annotations
from pydantic import BaseModel

class LabelBase(BaseModel):
    id: int
    title: str
    color: str

class LabelResponse(LabelBase):
    pass
