from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_notification_settings import UserNotificationSettingsCreate, UserNotificationSettingsUpdate, \
    UserNotificationSettingsResponse as UserNotificationSettings
from app.services.user_notification_settings_service import UserNotificationSettingsService

router = APIRouter()


@router.post("/user_notification_settings", response_model=UserNotificationSettings)
def create_user_notification_settings(user_notification_settings_in: UserNotificationSettingsCreate,
                                      db: Session = Depends(get_db)):
    service = UserNotificationSettingsService(db)
    return service.create_user_notification_settings(user_notification_settings_in)


@router.get("/user_notification_settings/{user_notification_settings_id}", response_model=UserNotificationSettings)
def get_user_notification_settings(user_notification_settings_id: str, db: Session = Depends(get_db)):
    service = UserNotificationSettingsService(db)
    user_notification_settings = service.get_user_notification_settings_by_id(user_notification_settings_id)
    if not user_notification_settings:
        raise HTTPException(status_code=404, detail="User Notification Settings not found")
    return user_notification_settings


@router.get("/user_notification_settings", response_model=list[UserNotificationSettings])
def get_all_user_notification_settings(db: Session = Depends(get_db)):
    service = UserNotificationSettingsService(db)
    return service.get_all_user_notification_settings()


@router.put("/user_notification_settings/{user_notification_settings_id}", response_model=UserNotificationSettings)
def update_user_notification_settings(user_notification_settings_id: str,
                                      user_notification_settings_in: UserNotificationSettingsUpdate,
                                      db: Session = Depends(get_db)):
    service = UserNotificationSettingsService(db)
    user_notification_settings = service.update_user_notification_settings(user_notification_settings_id,
                                                                           user_notification_settings_in)
    if not user_notification_settings:
        raise HTTPException(status_code=404, detail="User Notification Settings not found")
    return user_notification_settings


@router.delete("/user_notification_settings/{user_notification_settings_id}", status_code=204)
def delete_user_notification_settings(user_notification_settings_id: str, db: Session = Depends(get_db)):
    service = UserNotificationSettingsService(db)
    service.delete_user_notification_settings(user_notification_settings_id)
    return {"ok": True}
