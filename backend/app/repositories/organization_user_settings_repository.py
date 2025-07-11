from sqlalchemy.orm import Session

from app.db.models.organization_user_settings import OrganizationUserSettings


class OrganizationUserSettingsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, organization_user_settings: OrganizationUserSettings) -> OrganizationUserSettings:
        self.db.add(organization_user_settings)
        self.db.commit()
        self.db.refresh(organization_user_settings)
        return organization_user_settings

    def get_by_id(self, organization_user_settings_id: str) -> OrganizationUserSettings:
        return self.db.query(OrganizationUserSettings).filter(
            OrganizationUserSettings.id == organization_user_settings_id).first()

    def get_all(self) -> list[OrganizationUserSettings]:
        return self.db.query(OrganizationUserSettings).all()

    def update(self, organization_user_settings: OrganizationUserSettings) -> OrganizationUserSettings:
        self.db.merge(organization_user_settings)
        self.db.commit()
        self.db.refresh(organization_user_settings)
        return organization_user_settings

    def delete(self, organization_user_settings_id: str):
        organization_user_settings = self.db.query(OrganizationUserSettings).filter(
            OrganizationUserSettings.id == organization_user_settings_id).first()
        if organization_user_settings:
            self.db.delete(organization_user_settings)
            self.db.commit()
