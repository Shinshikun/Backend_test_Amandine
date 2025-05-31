from src.models.task import Label
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_label(db_session: AsyncSession, label_id: int) -> Label:
    label = (await db_session.scalars(select(Label).where(Label.id == label_id))).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label inexistant")
    return label

async def get_all_labels(db_session: AsyncSession) -> list[Label]:
    labels = (await db_session.scalars(select(Label))).all()
    return labels

def add_label(db_session: AsyncSession, label: Label):
    db_session.add(label)

async def delete_label(db_session: AsyncSession, label_id: int):
    label = await get_label(db_session, label_id)
    await db_session.delete(label)