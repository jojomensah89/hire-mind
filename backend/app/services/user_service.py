import uuid

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        user = User(**user_in.dict())
        user.id = str(uuid.uuid4())  # Generate a UUID for the user ID
        return self.user_repo.create(user)

    def get_user_by_id(self, user_id: str) -> User:
        return self.user_repo.get_by_id(user_id)

    def get_all_users(self) -> list[User]:
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_in: UserUpdate) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        for field, value in user_in.dict(exclude_unset=True).items():
            setattr(user, field, value)
        return self.user_repo.update(user)

    def delete_user(self, user_id: str):
        self.user_repo.delete(user_id)
