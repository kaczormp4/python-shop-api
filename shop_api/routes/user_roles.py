from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from shop.domain.entities.roles import UserRole
from shop.domain.services.user_roles import UserRolesService

from shop_api.auth.jwt import get_current_user
from shop_api.auth.permissions import require_permission
from shop_api.dependencies import get_user_roles_service
from shop_api.schemas.roles import RoleResponse

user_roles_router = APIRouter(
    prefix="/users",
    tags=["user roles"],
    dependencies=[Depends(get_current_user)],
)


@user_roles_router.post(
    "/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_role(
    user_id: UUID,
    role_id: UUID,
    service: UserRolesService = Depends(get_user_roles_service),
    _: dict = Depends(require_permission("roles.assign")),
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
    _: dict = Depends(require_permission("roles.unassign")),
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
    _: dict = Depends(require_permission("users.read")),
) -> list[UserRole]:
    try:
        return service.get_user_roles(user_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
