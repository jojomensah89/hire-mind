from datetime import datetime

from pydantic import EmailStr

from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    name: str
    image_url: str
    email: str


class UserCreate(UserBase):
    id: str


class UserUpdate(UserBase):
    name: str | None = None
    image_url: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
