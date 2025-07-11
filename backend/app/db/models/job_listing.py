from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin, UUIDMixin
from app.db.enums import WageIntervalEnum, LocationRequirementEnum, JobListingStatus, ExperienceLevelEnum, \
    JobListingStatusEnum, JobListingTypeEnum

wage_intervals = ["hourly", "yearly"]
location_requirements = ["in-office", "hybrid", "remote"]
experience_levels = ["junior", "mid-level", "senior"]
job_listing_statuses = ["draft", "published", "delisted"]
job_listing_types = ["internship", "part-time", "full-time"]


class JobListing(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "job_listings"

    organization_id = Column(String, ForeignKey("organizations.id", ondelete="cascade"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    wage = Column(Integer)
    wage_interval = Column(WageIntervalEnum)
    state_abbreviation = Column(String)
    city = Column(String)
    is_featured = Column(Boolean, nullable=False, default=False)
    location_requirement = Column(LocationRequirementEnum, nullable=False)
    experience_level = Column(ExperienceLevelEnum, nullable=False)
    status = Column(JobListingStatusEnum, nullable=False, default=JobListingStatus.DRAFT)
    type = Column(JobListingTypeEnum, nullable=False)
    posted_at = Column(DateTime(timezone=True))

    # Relationships
    organization = relationship("Organization", back_populates="job_listings")
    applications = relationship("JobListingApplication", back_populates="job_listing", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("ix_job_listings_state_abbreviation", "state_abbreviation"),
    )
