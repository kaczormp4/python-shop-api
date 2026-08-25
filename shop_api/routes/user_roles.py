from collections.abc import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from shop.domain.entities.roles import UserRole
from shop.domain.services.user_roles import UserRolesService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.roles import ImplRolesRepository
from shop.infrastructure.repositories.user_roles import (
    ImplUserRolesRepository,
)
from shop.infrastructure.repositories.users import ImplUsersRepository

from shop_api.schemas.roles import RoleResponse

user_roles_router = APIRouter(
    prefix="/users",
    tags=["user roles"],
)


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


@user_roles_router.post(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_role(
    user_id: UUID,
    role_id: UUID,
    service: UserRolesService = Depends(get_user_roles_service),
) -> None:
    try:
        service.assign_role(
            user_id,
            role_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@user_roles_router.delete(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_role(
    user_id: UUID,
    role_id: UUID,
    service: UserRolesService = Depends(get_user_roles_service),
) -> None:
    try:
        service.remove_role(
            user_id,
            role_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@user_roles_router.get(
    "/{user_id}/roles",
    response_model=list[RoleResponse],
)
def get_user_roles(
    user_id: UUID,
    service: UserRolesService = Depends(get_user_roles_service),
) -> list[UserRole]:
    try:
        return service.get_user_roles(user_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
