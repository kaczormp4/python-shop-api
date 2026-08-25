from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    surname: str
    email: str
