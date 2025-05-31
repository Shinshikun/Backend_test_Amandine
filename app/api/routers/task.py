from api.auth.auth import validate_is_authenticated
from api import DBSessionDep
from api.auth.user import CurrentUserDep
from src.pydantic.label import LabelBase
from src.models.task import Label, Task
from src.pydantic.task import TaskCreate, TaskResponse
from src.crud.task import add_labels_to_task, add_task, delete_task, get_all_tasks, get_task, remove_label_from_task
from fastapi import APIRouter, Body, Depends, HTTPException, status

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(validate_is_authenticated)])
async def tasks_details(db_session: DBSessionDep) -> list[TaskResponse]:
    return await get_all_tasks(db_session)



@router.get(
    "/{task_id}",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_200_OK
)
async def task_details(
    task_id: str,
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