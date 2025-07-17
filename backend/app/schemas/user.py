from datetime import datetime

from pydantic import EmailStr

from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    first_name: str | None = None
    last_name: str | None = None
    image_url: str | None = None
    phone_number: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    clerk_id: str


class UserUpdate(UserBase):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    image_url: str | None = None


class UserResponse(UserBase):
    id: str
    clerk_id: str
    created_at: datetime
    updated_at: datetime
