from datetime import datetime
from typing import Optional
from uuid import UUID

from app.db.enums import ApplicationStage
from app.schemas.base import BaseSchema
from app.schemas.job_listing import JobListingResponse
from app.schemas.user import UserResponse


class JobListingApplicationBase(BaseSchema):
    cover_letter: Optional[str] = None
    rating: Optional[int] = None
    stage: ApplicationStage = ApplicationStage.APPLIED


class JobListingApplicationCreate(JobListingApplicationBase):
    job_listing_id: UUID
    user_id: str


class JobListingApplicationUpdate(BaseSchema):
    cover_letter: Optional[str] = None
    rating: Optional[int] = None
    stage: Optional[ApplicationStage] = None


class JobListingApplicationResponse(JobListingApplicationBase):
    job_listing_id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
    job_listing: Optional[JobListingResponse] = None
    user: Optional[UserResponse] = None
