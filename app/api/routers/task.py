from sqlalchemy import select
from sqlalchemy.orm import selectinload
from api.auth.auth import validate_is_authenticated
from api import DBSessionDep
from api.auth.user import CurrentUserDep
from src.pydantic.label import LabelBase
from src.models.task import Label, Task
from src.pydantic.task import TaskCreate, TaskResponse, TaskUpdate
from src.crud.task import add_labels_to_task, add_task, delete_task, get_all_tasks, get_task, remove_label_from_task
from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(validate_is_authenticated)])
async def tasks_details(db_session: DBSessionDep) -> list[TaskResponse]:
    return await get_all_tasks(db_session)


@router.get("/search", dependencies=[Depends(validate_is_authenticated)], response_model=list[TaskResponse])
async def search_tasks(
    db_session: DBSessionDep,
    user: CurrentUserDep,
    created_within: str = Query(None, enum=["24h", "7d", "30d"]),
    title: str = Query(None),
    label_id: int = Query(None)
):
    query = select(Task)

    # Filtre par date
    if created_within:
        now = datetime.now()
        if created_within == "24h":
            since = now - timedelta(hours=24)
        elif created_within == "7d":
            since = now - timedelta(days=7)
        elif created_within == "30d":
            since = now - timedelta(days=30)
        query = query.where(Task.date >= since)

    # Filtre par titre
    if title:
        query = query.where(Task.description.ilike(f"%{title}%"))

    # Filtre par label
    if label_id:
        query = query.join(Task.labels).where(Label.id == label_id)

    query = query.options(selectinload(Task.labels))

    result = await db_session.execute(query)
    tasks = result.scalars().all()
    return tasks



@router.get(
    "/{task_id}",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_200_OK
)
async def task_details(
    task_id: int,
    db_session: DBSessionDep,
) -> TaskResponse:
    task = await get_task(db_session, task_id)
    return task



@router.post(
    "/create_task",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    new_task: TaskCreate,
    db_session: DBSessionDep,
    user: CurrentUserDep
) -> TaskResponse:
    task_bd = Task(description=new_task.description)
    task_bd.user = user
    labels_db: list[Label] = []

    for label_input in new_task.labels:
        if label_input.id:
            label = await db_session.get(Label, label_input.id)
            if label:
                labels_db.append(label)
        elif label_input.title:
            label = Label(title=label_input.title, color=label_input.color or "blue")
            db_session.add(label)
            await db_session.flush()  # Obtenir un id
            labels_db.append(label)

    task_bd.labels = labels_db
    db_session.add(task_bd)
    await db_session.commit()
    await db_session.refresh(task_bd)

    return task_bd


@router.delete("/{task_id}", dependencies=[Depends(validate_is_authenticated)])
async def delete_task_route(
    task_id: int,
    db_session: DBSessionDep,
    user: CurrentUserDep
):
    task = await get_task(db_session, task_id)
    if not user.is_superuser and task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Non autorisé à supprimer cette tâche")
    await delete_task(db_session, task)
    await db_session.commit()
    return {"detail": "Tâche supprimée"}


@router.patch("/{task_id}/remove-label/{label_id}", dependencies=[Depends(validate_is_authenticated)])
async def remove_label(
    task_id: int,
    label_id: int,
    db_session: DBSessionDep,
    user: CurrentUserDep
) -> TaskResponse:
    task = await get_task(db_session, task_id)
    if not user.is_superuser and task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Non autorisé à modifier cette tâche")

    await remove_label_from_task(task, label_id)
    await db_session.commit()
    return task


@router.patch("/{task_id}/add-labels", dependencies=[Depends(validate_is_authenticated)])
async def add_labels(
    task_id: int,
    db_session: DBSessionDep,
    user: CurrentUserDep,
    labels: list[LabelBase] = Body(...),
) -> TaskResponse:
    task = await get_task(db_session, task_id)
    if not user.is_superuser and task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Non autorisé à modifier cette tâche")

    labels_dicts = [label.model_dump(exclude_unset=True) for label in labels]
    await add_labels_to_task(db_session, task, labels_dicts)
    await db_session.commit()
    await db_session.refresh(task)
    return task



@router.post("/{task_id}/add_label", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def add_label_to_task(
    task_id: int,
    label_id: int,
    db_session: DBSessionDep,
    user: CurrentUserDep
):
    task = await get_task(db_session, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    label = await db_session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")

    if label not in task.labels:
        task.labels.append(label)
        await db_session.commit()
        await db_session.refresh(task)

    return task


@router.patch("/{task_id}", dependencies=[Depends(validate_is_authenticated)])
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db_session: DBSessionDep
) -> TaskResponse:
    task = await get_task(db_session, task_id)
    data_task = task_update.model_dump(exclude_unset=True)
    for key, value in data_task.items():
        setattr(task, key, value)

    await db_session.commit()
    return task
