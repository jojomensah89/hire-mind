from sqlalchemy.orm import Session

from app.db.models.user_resume import UserResume


class UserResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_resume: UserResume) -> UserResume:
        self.db.add(user_resume)
        self.db.commit()
        self.db.refresh(user_resume)
        return user_resume

    def get_by_id(self, user_resume_id: str) -> UserResume:
        return self.db.query(UserResume).filter(UserResume.id == user_resume_id).first()

    def get_all(self) -> list[UserResume]:
        return self.db.query(UserResume).all()

    def update(self, user_resume: UserResume) -> UserResume:
        self.db.merge(user_resume)
        self.db.commit()
        self.db.refresh(user_resume)
        return user_resume

    def delete(self, user_resume_id: str):
        user_resume = self.db.query(UserResume).filter(UserResume.id == user_resume_id).first()
        if user_resume:
            self.db.delete(user_resume)
            self.db.commit()
