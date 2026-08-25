from collections.abc import Generator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from shop.domain.services.orders import OrdersService
from shop.infrastructure.dependencies import get_uow
from shop.infrastructure.orm.orders import OrderModel
from shop.infrastructure.repositories.orders import ImplOrdersRepository

from shop_api.schemas.orders import (
    OrderCreate,
    OrderResponse,
    OrderUpdate,
)

orders_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


def get_orders_service() -> Generator[OrdersService, None, None]:
    with get_uow() as uow:
        repository = ImplOrdersRepository(uow)

        yield OrdersService(repository)


@orders_router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order: OrderCreate,
    service: OrdersService = Depends(get_orders_service),
) -> OrderModel:
    order_model = OrderModel(
        total_price=order.total_price,
        delivery_date=order.delivery_date,
        status=order.status,
    )

    try:
        return service.create_order(order_model)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@orders_router.get(
    "",
    response_model=list[OrderResponse],
)
def list_orders(
    service: OrdersService = Depends(get_orders_service),
) -> list[OrderModel]:
    return service.list_orders()


@orders_router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order_by_id(
    order_id: UUID,
    service: OrdersService = Depends(get_orders_service),
) -> OrderModel:
    try:
        return service.get_order_by_id(order_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@orders_router.put(
    "/{order_id}",
    response_model=OrderResponse,
)
def update_order(
    order_id: UUID,
    order: OrderUpdate,
    service: OrdersService = Depends(get_orders_service),
) -> OrderModel:
    order_model = OrderModel(
        total_price=order.total_price,
        delivery_date=order.delivery_date,
        status=order.status,
    )

    try:
        return service.update_order(
            order_id,
            order_model,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@orders_router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    order_id: UUID,
    service: OrdersService = Depends(get_orders_service),
) -> None:
    try:
        service.delete_order(order_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
