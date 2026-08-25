from uuid import UUID

from pydantic import BaseModel
from shop.domain.entities.roles import UserRoles


class RoleCreate(BaseModel):
    role: UserRoles


class RoleResponse(BaseModel):
    id: UUID
    role: UserRoles
