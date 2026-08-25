from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from shop.domain.entities.orders import OrderStatus


class OrderCreate(BaseModel):
    total_price: Decimal
    delivery_date: datetime | None = None
    status: OrderStatus = OrderStatus.ORDERED


class OrderUpdate(BaseModel):
    total_price: Decimal
    delivery_date: datetime | None = None
    status: OrderStatus


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    creation_date: datetime
    delivery_date: datetime | None
    total_price: Decimal
    status: OrderStatus
