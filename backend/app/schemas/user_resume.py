from datetime import datetime
from typing import Optional

from app.schemas.base import BaseSchema


class UserResumeBase(BaseSchema):
    resume_file_url: str
    resume_file_key: str
    ai_summary: Optional[str] = None


class UserResumeCreate(UserResumeBase):
    user_id: str


class UserResumeUpdate(BaseSchema):
    resume_file_url: Optional[str] = None
    resume_file_key: Optional[str] = None
    ai_summary: Optional[str] = None


class UserResumeResponse(UserResumeBase):
    user_id: str
    created_at: datetime
    updated_at: datetime
