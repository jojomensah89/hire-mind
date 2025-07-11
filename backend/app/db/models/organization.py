from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    image_url = Column(String)

    # Relationships
    job_listings = relationship("JobListing", back_populates="organization", cascade="all, delete-orphan")
    organization_user_settings = relationship("OrganizationUserSettings", back_populates="organization",
                                              cascade="all, delete-orphan")
