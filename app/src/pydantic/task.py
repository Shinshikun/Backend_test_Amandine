from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Import réel (pas seulement pour TYPE_CHECKING)
from src.pydantic.label import LabelBase

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str
    labels: list[LabelBase]

class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: int

class TaskCreate(BaseModel):
    description: str
    labels: Optional[list[LabelBase]] = []


