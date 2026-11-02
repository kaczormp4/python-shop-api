from fastapi import Depends, HTTPException, status
from shop.domain.services.user_roles import UserRolesService
from shop_api.auth.acl import get_role_permissions
from shop_api.auth.jwt import get_current_user
from shop_api.dependencies import get_user_roles_service


def require_permission(
    required_permission: str,
):
    def dependency(
        current_user=Depends(get_current_user),
        service: UserRolesService = Depends(get_user_roles_service),
    ):
        user_roles = service.get_user_roles(current_user["sub"])

        role_names = [user_role.role.value for user_role in user_roles]

        user_permissions = set()

        for role_name in role_names:
            user_permissions.update(get_role_permissions(role_name))

        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return dependency
