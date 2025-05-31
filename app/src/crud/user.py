from src.models.task import Task
from src.models.user import User
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(db_session: AsyncSession, user_id: int) -> User:
    stmt = (
        select(User)
        .options(
            selectinload(User.tasks).selectinload(Task.labels)
        )
        .where(User.id == user_id)
    )
    user = (await db_session.scalars(stmt)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")
    return user


async def get_all_users(db_session: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .options(
            selectinload(User.tasks).selectinload(Task.labels)
        )
    )
    users = (await db_session.scalars(stmt)).all()
    return users


async def get_user_by_email(db_session: AsyncSession, email: str) -> User | None:
    return (await db_session.scalars(select(User).where(User.email == email))).first()


def add_user(db_session: AsyncSession, user: User):
    db_session.add(user)

def update_user(db_session: AsyncSession, user: User):
    pass