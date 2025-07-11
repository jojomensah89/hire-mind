from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class UserNotificationSettings(Base, TimestampMixin):
    __tablename__ = "user_notification_settings"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True, nullable=False)
    new_job_email_notifications = Column(Boolean, nullable=False, default=False)
    ai_prompt = Column(String)

    # Relationships
    user = relationship("User", back_populates="notification_settings")
