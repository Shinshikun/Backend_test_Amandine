from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.api import DBSessionDep
from app.src.crud.user import add_user, get_user_by_email
from app.src.pydantic.auth import Token
from app.src.models.user import User
from app.src.pydantic.user import UserCreate, UserPrivate, UserResponse
from app.utils.auth import create_access_token, verify_password

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: DBSessionDep) -> Token:
    user: User = await get_user_by_email(db_session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Identifiants incorrectes")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(new_user: UserCreate, db_session: DBSessionDep) -> UserPrivate:
    if (await db_session.scalars(select(User).where(User.email == new_user.email))).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà existant")

    user_bd = User(**new_user.model_dump())
    add_user(db_session, user_bd)
    await db_session.commit()
    
    return user_bd
    