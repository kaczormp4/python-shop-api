from fastapi import APIRouter
from shop.domain.services.products import ProductsService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.repositories.products import ImplProductsRepository

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


def get_products_service() -> ProductsService:
    with get_uow() as uow:
        repository = ImplProductsRepository(uow)
        return ProductsService(repository)
