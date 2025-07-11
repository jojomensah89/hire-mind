from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint, Text
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin
from app.db.enums import ApplicationStage, ApplicationStageEnum

application_stages = ["denied", "applied", "interested", "interviewed", "hired"]


class JobListingApplication(Base, TimestampMixin):
    __tablename__ = "job_listing_applications"

    job_listing_id = Column(String, ForeignKey("job_listings.id", ondelete="cascade"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    cover_letter = Column(Text)
    rating = Column(Integer)
    stage = Column(ApplicationStageEnum, nullable=False, default=ApplicationStage.APPLIED)

    # Composite primary key
    __table_args__ = (
        PrimaryKeyConstraint("job_listing_id", "user_id"),
    )

    # Relationships
    job_listing = relationship("JobListing", back_populates="applications")
    user = relationship("User", back_populates="applications")
