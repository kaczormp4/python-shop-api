from fastapi import APIRouter, Depends, HTTPException, status

from shop.domain.entities import Product
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


@router.post(
    "",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: Product,
    service: ProductsService = Depends(get_products_service),
) -> Product:
    try:
        return service.create_product(product)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[Product],
)
def list_products(
    service: ProductsService = Depends(get_products_service),
) -> list[Product]:
    return service.list_products()


@router.get(
    "/{product_id}",
    response_model=Product,
)
def get_product_by_id(
    product_id: str,
    service: ProductsService = Depends(get_products_service),
) -> Product:
    try:
        return service.get_product_by_id(product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.put(
    "/{product_id}",
    response_model=Product,
)
def update_product(
    product_id: str,
    product: Product,
    service: ProductsService = Depends(get_products_service),
) -> Product:
    try:
        return service.update_product(
            product_id,
            product,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: str,
    service: ProductsService = Depends(get_products_service),
) -> None:
    try:
        service.delete_product(product_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc