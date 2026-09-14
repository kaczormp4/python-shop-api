from collections.abc import Generator

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from shop.domain.entities.users import User
from shop.domain.services.users import UsersService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.users import ImplUsersRepository

from shop_api.schemas.users import UserCreate


def get_users_service() -> Generator[UsersService, None, None]:
    with get_uow() as uow:
        repository = ImplUsersRepository(uow)

        yield UsersService(repository)


public_router = APIRouter(
    prefix="/public",
    tags=["public"],
)


class Login(BaseModel):
    email: str
    password: str


@public_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: UserCreate,
    service: UsersService = Depends(get_users_service),
) -> None:
    domain_user = User(
        name=user.name, surname=user.surname, email=user.email, password=user.password
    )

    return service.create_user(domain_user)


@public_router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
)
def login_user(
    login: Login,
    service: UsersService = Depends(get_users_service),
) -> None:
    # tu dokonczyc
    # return service.create_user(domain_user)
