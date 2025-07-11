from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class OrganizationUserSettingsBase(BaseSchema):
    new_application_email_notifications: bool = False
    minimum_rating: Optional[int] = None


class OrganizationUserSettingsCreate(OrganizationUserSettingsBase):
    user_id: str
    organization_id: str


class OrganizationUserSettingsUpdate(BaseSchema):
    new_application_email_notifications: Optional[bool] = None
    minimum_rating: Optional[int] = None


class OrganizationUserSettingsResponse(OrganizationUserSettingsBase):
    user_id: str
    organization_id: str
    created_at: datetime
    updated_at: datetime
