from collections.abc import Generator
from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from shop.domain.entities.users import User
from shop.domain.services.user_roles import UserRolesService
from shop.domain.services.users import UsersService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.roles import ImplRolesRepository
from shop.infrastructure.repositories.user_roles import (
    ImplUserRolesRepository,
)
from shop.infrastructure.repositories.users import ImplUsersRepository

from shop_api.auth.jwt import get_current_user
from shop_api.schemas.users import (
    UserCreate,
    UserResponse,
)

users_router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user)])


def get_users_service() -> Generator[UsersService, None, None]:
    with get_uow() as uow:
        repository = ImplUsersRepository(uow)

        yield UsersService(repository)


def get_user_roles_service() -> Generator[
    UserRolesService,
    None,
    None,
]:
    with get_uow() as uow:
        user_roles_repository = ImplUserRolesRepository(uow)
        users_repository = ImplUsersRepository(uow)
        roles_repository = ImplRolesRepository(uow)

        yield UserRolesService(
            user_roles_repository,
            users_repository,
            roles_repository,
        )


def require_role(
    required_roles: list[str],
    current_user=Depends(get_current_user),
    service: UserRolesService = Depends(get_user_roles_service),
):
    current_timestamp = datetime.now(UTC).timestamp()

    if current_user["exp"] < current_timestamp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    user_roles = service.get_user_roles(current_user["sub"])

    user_role_names = [user_role.role.value for user_role in user_roles]

    for required_role in required_roles:
        if required_role not in user_role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

    return current_user


@users_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    service: UsersService = Depends(get_users_service),
) -> User:
    domain_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
    )

    return service.create_user(domain_user)


@users_router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    service: UsersService = Depends(get_users_service),
) -> list[User]:
    return service.list_users()


@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    user_id: UUID,
    service: UsersService = Depends(get_users_service),
    _: str = Depends(require_role(["ADMIN"])),
) -> User:
    try:
        return service.get_user_by_id(user_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: UUID,
    service: UsersService = Depends(get_users_service),
) -> None:
    try:
        service.delete_user(user_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
