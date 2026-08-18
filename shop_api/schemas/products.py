from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from shop.domain.entities.products import ProductCategory


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    category: ProductCategory
    price: Decimal
    quantity_stock: int


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category: ProductCategory
    price: Decimal
    quantity_stock: int
