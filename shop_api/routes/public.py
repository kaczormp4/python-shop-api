from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from shop.domain.entities.users import User
from shop.domain.services.users import UsersService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.users import ImplUsersRepository
from shop.infrastructure.security.jwt import create_access_token

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
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
    )

    try:
        return service.create_user(domain_user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@public_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
def login_user(
    login: Login,
    service: UsersService = Depends(get_users_service),
) -> dict:
    try:
        user = service.login_user(
            login.email,
            login.password,
        )

        return create_access_token(str(user.id), user.email)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
