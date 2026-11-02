from collections.abc import Generator

from shop.domain.services.user_roles import UserRolesService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.roles import ImplRolesRepository
from shop.infrastructure.repositories.user_roles import (
    ImplUserRolesRepository,
)
from shop.infrastructure.repositories.users import ImplUsersRepository


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
