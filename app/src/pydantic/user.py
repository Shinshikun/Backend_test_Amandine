from pydantic import BaseModel, ConfigDict, field_validator

from utils.auth import hash_password

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

    @field_validator('password')
    def hash_user_password(cls, password):
        return hash_password(password)


class UserPrivate(UserBase):
    password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nom: str | None = None
    prenom: str | None = None
    email: str | None = None
    is_superuser: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)