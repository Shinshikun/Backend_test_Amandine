from fastapi import APIRouter, Depends, status
from app.api.auth.auth import validate_is_authenticated
from app.api import DBSessionDep
from app.src.pydantic.label import LabelBase, LabelCreate, LabelResponse, LabelUpdate
from app.src.models.task import Label
from app.src.crud.label import get_all_labels, get_label, add_label, delete_label

router = APIRouter(
    prefix="/api/labels",
    tags=["labels"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", dependencies=[Depends(validate_is_authenticated)])
async def list_labels(db_session: DBSessionDep) -> list[LabelBase]:
    return await get_all_labels(db_session)

@router.get("/{label_id}", dependencies=[Depends(validate_is_authenticated)])
async def get_one_label(label_id: int, db_session: DBSessionDep) -> LabelBase:
    return await get_label(db_session, label_id)

@router.post("/", dependencies=[Depends(validate_is_authenticated)], status_code=status.HTTP_201_CREATED)
async def create_label(label: LabelCreate, db_session: DBSessionDep) -> LabelBase:
    label_obj = Label(**label.model_dump())
    add_label(db_session, label_obj)
    await db_session.commit()
    return label_obj

@router.delete("/{label_id}", dependencies=[Depends(validate_is_authenticated)], status_code=status.HTTP_204_NO_CONTENT)
async def remove_label(label_id: int, db_session: DBSessionDep):
    await delete_label(db_session, label_id)
    await db_session.commit()


@router.patch("/{label_id}", dependencies=[Depends(validate_is_authenticated)])
async def update_label(
    label_id: int,
    label_update: LabelUpdate,
    db_session: DBSessionDep
) -> LabelResponse:
    label = await get_label(db_session, label_id)
    data_label = label_update.model_dump(exclude_unset=True)
    for key, value in data_label.items():
        setattr(label, key, value)

    await db_session.commit()
    return label