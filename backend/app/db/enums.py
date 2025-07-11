import enum

from sqlalchemy import Enum as SQLEnum


class WageInterval(enum.Enum):
    HOURLY = "hourly"
    YEARLY = "yearly"


class LocationRequirement(enum.Enum):
    IN_OFFICE = "in-office"
    HYBRID = "hybrid"
    REMOTE = "remote"


class ExperienceLevel(enum.Enum):
    JUNIOR = "junior"
    MID_LEVEL = "mid-level"
    SENIOR = "senior"


class JobListingStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELISTED = "delisted"


class JobListingType(enum.Enum):
    INTERNSHIP = "internship"
    PART_TIME = "part-time"
    FULL_TIME = "full-time"


class ApplicationStage(enum.Enum):
    DENIED = "denied"
    APPLIED = "applied"
    INTERESTED = "interested"
    INTERVIEWED = "interviewed"
    HIRED = "hired"


# SQLAlchemy enum types
WageIntervalEnum = SQLEnum(WageInterval, name="job_listings_wage_interval")
LocationRequirementEnum = SQLEnum(LocationRequirement, name="job_listings_location_requirement")
ExperienceLevelEnum = SQLEnum(ExperienceLevel, name="job_listings_experience_level")
JobListingStatusEnum = SQLEnum(JobListingStatus, name="job_listings_status")
JobListingTypeEnum = SQLEnum(JobListingType, name="job_listings_type")
ApplicationStageEnum = SQLEnum(ApplicationStage, name="job_listing_applications_stage")
