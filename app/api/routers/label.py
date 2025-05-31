from fastapi import APIRouter, Depends, status
from api.auth.auth import validate_is_authenticated
from api import DBSessionDep
from src.pydantic.label import LabelBase
from src.models.task import Label
from src.crud.label import get_all_labels, get_label, add_label, delete_label

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
async def create_label(label: LabelBase, db_session: DBSessionDep) -> LabelBase:
    label_obj = Label(**label.model_dump())
    add_label(db_session, label_obj)
    await db_session.commit()
    return label_obj

@router.delete("/{label_id}", dependencies=[Depends(validate_is_authenticated)], status_code=status.HTTP_204_NO_CONTENT)
async def remove_label(label_id: int, db_session: DBSessionDep):
    await delete_label(db_session, label_id)
    await db_session.commit()