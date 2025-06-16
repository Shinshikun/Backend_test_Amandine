from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_serializer

# Import réel (pas seulement pour TYPE_CHECKING)
from src.pydantic.label import LabelBase

class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str
    labels: list[LabelBase]
    title: str
    date: datetime

    @model_serializer
    def default_title_serializer(self) -> dict:
        data = self.__dict__.copy()
        if not data.get("title"):
            desc = data.get("description", "")
            data["title"] = (desc[:10] + "...") if len(desc) > 10 else desc
        return data

class TaskResponse(TaskBase):
    user_id: int

class TaskCreate(BaseModel):
    title: Optional[str] = None
    labels: Optional[list[LabelBase]] = []
    description: Optional[str] = None


