from sqlalchemy.orm import Session

from app.db.models.user_notification_settings import UserNotificationSettings


class UserNotificationSettingsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_notification_settings: UserNotificationSettings) -> UserNotificationSettings:
        self.db.add(user_notification_settings)
        self.db.commit()
        self.db.refresh(user_notification_settings)
        return user_notification_settings

    def get_by_id(self, user_notification_settings_id: str) -> UserNotificationSettings:
        return self.db.query(UserNotificationSettings).filter(
            UserNotificationSettings.id == user_notification_settings_id).first()

    def get_all(self) -> list[UserNotificationSettings]:
        return self.db.query(UserNotificationSettings).all()

    def update(self, user_notification_settings: UserNotificationSettings) -> UserNotificationSettings:
        self.db.merge(user_notification_settings)
        self.db.commit()
        self.db.refresh(user_notification_settings)
        return user_notification_settings

    def delete(self, user_notification_settings_id: str):
        user_notification_settings = self.db.query(UserNotificationSettings).filter(
            UserNotificationSettings.id == user_notification_settings_id).first()
        if user_notification_settings:
            self.db.delete(user_notification_settings)
            self.db.commit()
