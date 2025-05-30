from src.models.user import User
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(db_session: AsyncSession, user_id: int) -> User | None:
    user = (await db_session.scalars(select(User).where(User.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")
    return user


async def get_user_by_email(db_session: AsyncSession, email: str) -> User | None:
    return (await db_session.scalars(select(User).where(User.email == email))).first()


def add_user(db_session: AsyncSession, user: User):
    db_session.add(user)

def update_user(db_session: AsyncSession, user: User):
    db_session.get_one()