from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class OrganizationUserSettings(Base, TimestampMixin):
    __tablename__ = "organization_user_settings"

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id"), nullable=False)
    new_application_email_notifications = Column(Boolean, nullable=False, default=False)
    minimum_rating = Column(Integer)

    # Composite primary key
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "organization_id"),
    )

    # Relationships
    user = relationship("User", back_populates="organization_user_settings")
    organization = relationship("Organization", back_populates="organization_user_settings")
