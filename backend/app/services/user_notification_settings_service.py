import uuid

from sqlalchemy.orm import Session

from app.db.models.user_notification_settings import UserNotificationSettings
from app.repositories.user_notification_settings_repository import UserNotificationSettingsRepository
from app.schemas.user_notification_settings import UserNotificationSettingsCreate, UserNotificationSettingsUpdate


class UserNotificationSettingsService:
    def __init__(self, db: Session):
        self.user_notification_settings_repo = UserNotificationSettingsRepository(db)

    def create_user_notification_settings(self,
                                          user_notification_settings_in: UserNotificationSettingsCreate) -> UserNotificationSettings:
        user_notification_settings = UserNotificationSettings(**user_notification_settings_in.dict())
        user_notification_settings.id = str(uuid.uuid4())
        return self.user_notification_settings_repo.create(user_notification_settings)

    def get_user_notification_settings_by_id(self, user_notification_settings_id: str) -> UserNotificationSettings:
        return self.user_notification_settings_repo.get_by_id(user_notification_settings_id)

    def get_all_user_notification_settings(self) -> list[UserNotificationSettings]:
        return self.user_notification_settings_repo.get_all()

    def update_user_notification_settings(self, user_notification_settings_id: str,
                                          user_notification_settings_in: UserNotificationSettingsUpdate) -> UserNotificationSettings:
        user_notification_settings = self.user_notification_settings_repo.get_by_id(user_notification_settings_id)
        if not user_notification_settings:
            return None
        for field, value in user_notification_settings_in.dict(exclude_unset=True).items():
            setattr(user_notification_settings, field, value)
        return self.user_notification_settings_repo.update(user_notification_settings)

    def delete_user_notification_settings(self, user_notification_settings_id: str):
        self.user_notification_settings_repo.delete(user_notification_settings_id)
