from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class UserNotificationSettingsBase(BaseSchema):
    new_job_email_notifications: bool = False
    ai_prompt: Optional[str] = None


class UserNotificationSettingsCreate(UserNotificationSettingsBase):
    user_id: str


class UserNotificationSettingsUpdate(BaseSchema):
    new_job_email_notifications: Optional[bool] = None
    ai_prompt: Optional[str] = None


class UserNotificationSettingsResponse(UserNotificationSettingsBase):
    user_id: str
    created_at: datetime
    updated_at: datetime
