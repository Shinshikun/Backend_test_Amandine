from app.src.models.task import Task, Label
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

async def get_task(db_session: AsyncSession, task_id: int) -> Task:
    stmt = (
        select(Task)
        .options(selectinload(Task.labels))
        .where(Task.id == task_id)
    )
    task = (await db_session.scalars(stmt)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task inexistante")
    return task


async def get_all_tasks(db_session: AsyncSession) -> list[Task]:
    stmt = select(Task).options(selectinload(Task.labels))
    tasks = (await db_session.scalars(stmt)).all()
    return tasks


def add_task(db_session: AsyncSession, task: Task):
    db_session.add(task)

async def add_task_with_labels(
    db_session: AsyncSession,
    description: str,
    label_ids: list[int],
    user_id: int,
) -> Task:
    labels = []
    if label_ids:
        label_stmt = select(Label).where(Label.id.in_(label_ids))
        labels = (await db_session.scalars(label_stmt)).all()

    task = Task(description=description, labels=labels, user_id=user_id)
    db_session.add(task)
    return task

async def delete_task(db_session: AsyncSession, task: Task):
    await db_session.delete(task)

async def remove_label_from_task(task: Task, label_id: int):
    task.labels = [label for label in task.labels if label.id != label_id]


async def add_labels_to_task(
    db_session: AsyncSession,
    task: Task,
    labels_to_add: list[dict]
):
    for label_input in labels_to_add:
        label = None
        label_id = label_input.get("id")
        title = label_input.get("title")
        color = label_input.get("color", "blue")

        if label_id:
            label = await db_session.get(Label, label_id)
        elif title:
            label = Label(title=title, color=color)
            db_session.add(label)
            await db_session.flush()

        if label and label not in task.labels:
            task.labels.append(label)