import uuid

from sqlalchemy.orm import Session

from app.db.models.user_resume import UserResume
from app.repositories.user_resume_repository import UserResumeRepository
from app.schemas.user_resume import UserResumeCreate, UserResumeUpdate


class UserResumeService:
    def __init__(self, db: Session):
        self.user_resume_repo = UserResumeRepository(db)

    def create_user_resume(self, user_resume_in: UserResumeCreate) -> UserResume:
        user_resume = UserResume(**user_resume_in.dict())
        user_resume.id = str(uuid.uuid4())
        return self.user_resume_repo.create(user_resume)

    def get_user_resume_by_id(self, user_resume_id: str) -> UserResume:
        return self.user_resume_repo.get_by_id(user_resume_id)

    def get_all_user_resumes(self) -> list[UserResume]:
        return self.user_resume_repo.get_all()

    def update_user_resume(self, user_resume_id: str, user_resume_in: UserResumeUpdate) -> UserResume:
        user_resume = self.user_resume_repo.get_by_id(user_resume_id)
        if not user_resume:
            return None
        for field, value in user_resume_in.dict(exclude_unset=True).items():
            setattr(user_resume, field, value)
        return self.user_resume_repo.update(user_resume)

    def delete_user_resume(self, user_resume_id: str):
        self.user_resume_repo.delete(user_resume_id)
