from api.auth.auth import validate_is_authenticated
from api import DBSessionDep
from src.crud.user import get_user
from src.pydantic.user import UserResponse, UserUpdate
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/{user_id}",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_200_OK
)
async def user_details(
    user_id: str,
    db_session: DBSessionDep,
) -> UserResponse:
    user = await get_user(db_session, user_id)
    return UserResponse.model_validate(user)


@router.post(
    "/{user_id}",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_id: str,
):
    pass

@router.patch(
    "/{user_id}",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db_session: DBSessionDep
) -> UserResponse:
    data_user = user_update.model_dump(exclude_unset=True)
    user = await get_user(db_session, user_id)
    for key, value in data_user.items():
        setattr(user, key, value)

    db_session.commit()

    return UserResponse.model_validate(user)