from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base, TimestampMixin


class UserResume(Base, TimestampMixin):
    __tablename__ = "user_resumes"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True, nullable=False)
    resume_file_url = Column(String, nullable=False)
    resume_file_key = Column(String, nullable=False)
    ai_summary = Column(String)

    # Relationships
    user = relationship("User", back_populates="resume")
