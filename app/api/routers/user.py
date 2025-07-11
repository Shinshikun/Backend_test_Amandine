from app.api.auth.auth import validate_is_authenticated
from app.api import DBSessionDep
from app.src.crud.user import get_all_users, get_user
from app.src.pydantic.user import UserResponse, UserUpdate
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_200_OK
)
async def users_details(
    db_session: DBSessionDep,
) -> list[UserResponse]:
    users = await get_all_users(db_session)
    return users


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
    return user


@router.post(
    "/{user_id}",
    dependencies=[Depends(validate_is_authenticated)],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_id: str,
):
    pass

@router.patch("/{user_id}", dependencies=[Depends(validate_is_authenticated)])
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db_session: DBSessionDep
) -> UserResponse:
    user = await get_user(db_session, user_id)
    data_user = user_update.model_dump(exclude_unset=True)
    for key, value in data_user.items():
        setattr(user, key, value)

    await db_session.commit()
    return user