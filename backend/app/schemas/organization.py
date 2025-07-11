# Organization schemas
from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class OrganizationBase(BaseSchema):
    name: str
    image_url: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    id: str


class OrganizationUpdate(OrganizationBase):
    name: str | None = None
    image_url: str | None = None


class OrganizationResponse(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: datetime
