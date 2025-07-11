from .user import CurrentUserDep
from app.src.models.user import User


async def validate_is_authenticated(
    current_user: CurrentUserDep,
) -> User:
    return current_user