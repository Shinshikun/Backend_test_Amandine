from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.src.pydantic.task import TaskBase


class UserBase(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    is_superuser: bool = False

class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    password: str
    tasks: list[TaskBase] = Field(default_factory=list)

    @field_validator('password')
    def hash_user_password(cls, password):
        from app.utils.auth import hash_password
        return hash_password(password)

class UserPrivate(UserBase):
    password: str

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[str] = None
    is_superuser: Optional[bool] = None
    tasks: Optional[list[TaskBase]] = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    tasks: Optional[list[TaskBase]] = []