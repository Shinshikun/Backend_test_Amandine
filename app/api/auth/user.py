from typing import Annotated

from src.models.user import User
from api import DBSessionDep
from src.crud.user import get_user_by_email
from src.models.auth import TokenData
from utils.auth import decode_jwt, oauth2_scheme
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: DBSessionDep) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token manquant",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = decode_jwt(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError as e:
        raise credentials_exception
    user = await get_user_by_email(db_session, token_data.email)
    if user is None:
        raise credentials_exception
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]