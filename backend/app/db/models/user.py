from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    image_url = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    # Relationships
    notification_settings = relationship("UserNotificationSettings", back_populates="user", uselist=False,
                                         cascade="all, delete-orphan")
    resume = relationship("UserResume", back_populates="user", uselist=False, cascade="all, delete-orphan")
    organization_user_settings = relationship("OrganizationUserSettings", back_populates="user",
                                              cascade="all, delete-orphan")
    applications = relationship("JobListingApplication", back_populates="user", cascade="all, delete-orphan")
