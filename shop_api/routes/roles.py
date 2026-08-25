from collections.abc import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from shop.domain.entities.roles import UserRole
from shop.domain.services.roles import RolesService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.roles import ImplRolesRepository

from shop_api.schemas.roles import (
    RoleCreate,
    RoleResponse,
)

roles_router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


def get_roles_service() -> Generator[RolesService, None, None]:
    with get_uow() as uow:
        repository = ImplRolesRepository(uow)

        yield RolesService(repository)


@roles_router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role(
    role: RoleCreate,
    service: RolesService = Depends(get_roles_service),
) -> UserRole:
    domain_role = UserRole(
        role=role.role,
    )

    return service.create_role(domain_role)


@roles_router.get(
    "",
    response_model=list[RoleResponse],
)
def list_roles(
    service: RolesService = Depends(get_roles_service),
) -> list[UserRole]:
    return service.list_roles()


@roles_router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role_by_id(
    role_id: UUID,
    service: RolesService = Depends(get_roles_service),
) -> UserRole:
    try:
        return service.get_role_by_id(role_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@roles_router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_role(
    role_id: UUID,
    service: RolesService = Depends(get_roles_service),
) -> None:
    try:
        service.delete_role(role_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
