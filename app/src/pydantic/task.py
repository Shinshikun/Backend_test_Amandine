from __future__ import annotations
from enum import Enum, auto
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, model_serializer

# Import réel (pas seulement pour TYPE_CHECKING)
from app.src.pydantic.label import LabelBase

class TaskState(Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    ABANDONNED = "ABANDONNED"



class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str
    labels: list[LabelBase]
    title: str
    date: datetime
    etat: TaskState = TaskState.CREATED

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
    etat: TaskState = TaskState.CREATED


class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    description: Optional[str] = None
    labels: Optional[list[LabelBase]] = None
    title: Optional[str] = None
    etat: Optional[TaskState] = None


