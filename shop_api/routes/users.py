from collections.abc import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from shop.domain.entities.users import User
from shop.domain.services.users import UsersService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.users import ImplUsersRepository

from shop_api.schemas.users import (
    UserCreate,
    UserResponse,
)

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_users_service() -> Generator[UsersService, None, None]:
    with get_uow() as uow:
        repository = ImplUsersRepository(uow)

        yield UsersService(repository)


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
