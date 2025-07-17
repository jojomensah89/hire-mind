import uuid

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        user = User(
            id=str(uuid.uuid4()),
            **user_in.dict()
        )
        return self.user_repo.create(user)

    def get_user_by_id(self, user_id: str) -> User:
        return self.user_repo.get_by_id(user_id)

    def get_user_by_clerk_id(self, clerk_id: str) -> User:
        return self.user_repo.get_by_clerk_id(clerk_id)

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

    def create_user_from_webhook(self, user_data: dict) -> User:
        user_in = UserCreate(
            clerk_id=user_data.get('id'),
            email=user_data.get('email_addresses', [{}])[0].get('email_address'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            phone_number=user_data.get('phone_numbers', [{}])[0].get('phone_number'),
            image_url=user_data.get('image_url'),
        )
        return self.create_user(user_in)

    def update_user_from_webhook(self, user_data: dict) -> User:
        clerk_id = user_data.get('id')
        user = self.user_repo.get_by_clerk_id(clerk_id)
        if not user:
            return None

        user_in = UserUpdate(
            email=user_data.get('email_addresses', [{}])[0].get('email_address'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            phone_number=user_data.get('phone_numbers', [{}])[0].get('phone_number'),
            image_url=user_data.get('image_url'),
        )
        return self.update_user(user.id, user_in)

    def delete_user_from_webhook(self, user_data: dict):
        clerk_id = user_data.get('id')
        user = self.user_repo.get_by_clerk_id(clerk_id)
        if user:
            self.delete_user(user.id)
