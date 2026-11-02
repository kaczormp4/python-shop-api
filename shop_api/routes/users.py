from collections.abc import Generator
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
from shop_api.auth.permissions import require_permission
from shop_api.schemas.users import (
    UserCreate,
    UserResponse,
)

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)


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


@users_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    service: UsersService = Depends(get_users_service),
    _: dict = Depends(require_permission("users.create")),
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
    _: dict = Depends(require_permission("users.read")),
) -> list[User]:
    return service.list_users()


@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    user_id: UUID,
    service: UsersService = Depends(get_users_service),
    _: dict = Depends(require_permission("users.read")),
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
    _: dict = Depends(require_permission("users.delete")),
) -> None:
    try:
        service.delete_user(user_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
