from datetime import datetime
from typing import Optional
from uuid import UUID

from app.db.enums import WageInterval, LocationRequirement, ExperienceLevel, JobListingStatus, JobListingType
from app.schemas.base import BaseSchema
from app.schemas.organization import OrganizationResponse


class JobListingBase(BaseSchema):
    title: str
    description: str
    wage: Optional[int] = None
    wage_interval: Optional[WageInterval] = None
    state_abbreviation: Optional[str] = None
    city: Optional[str] = None
    is_featured: bool = False
    location_requirement: LocationRequirement
    experience_level: ExperienceLevel
    status: JobListingStatus = JobListingStatus.DRAFT
    type: JobListingType
    posted_at: Optional[datetime] = None


class JobListingCreate(JobListingBase):
    organization_id: str


class JobListingUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    wage: Optional[int] = None
    wage_interval: Optional[WageInterval] = None
    state_abbreviation: Optional[str] = None
    city: Optional[str] = None
    is_featured: Optional[bool] = None
    location_requirement: Optional[LocationRequirement] = None
    experience_level: Optional[ExperienceLevel] = None
    status: Optional[JobListingStatus] = None
    type: Optional[JobListingType] = None
    posted_at: Optional[datetime] = None


class JobListingResponse(JobListingBase):
    id: UUID
    organization_id: str
    created_at: datetime
    updated_at: datetime
    organization: Optional[OrganizationResponse] = None
