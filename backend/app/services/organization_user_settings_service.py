import uuid

from sqlalchemy.orm import Session

from app.db.models.organization_user_settings import OrganizationUserSettings
from app.repositories.organization_user_settings_repository import OrganizationUserSettingsRepository
from app.schemas.organization_user_settings import OrganizationUserSettingsCreate, OrganizationUserSettingsUpdate


class OrganizationUserSettingsService:
    def __init__(self, db: Session):
        self.organization_user_settings_repo = OrganizationUserSettingsRepository(db)

    def create_organization_user_settings(self,
                                          organization_user_settings_in: OrganizationUserSettingsCreate) -> OrganizationUserSettings:
        organization_user_settings = OrganizationUserSettings(**organization_user_settings_in.dict())
        organization_user_settings.id = str(uuid.uuid4())
        return self.organization_user_settings_repo.create(organization_user_settings)

    def get_organization_user_settings_by_id(self, organization_user_settings_id: str) -> OrganizationUserSettings:
        return self.organization_user_settings_repo.get_by_id(organization_user_settings_id)

    def get_all_organization_user_settings(self) -> list[OrganizationUserSettings]:
        return self.organization_user_settings_repo.get_all()

    def update_organization_user_settings(self, organization_user_settings_id: str,
                                          organization_user_settings_in: OrganizationUserSettingsUpdate) -> OrganizationUserSettings:
        organization_user_settings = self.organization_user_settings_repo.get_by_id(organization_user_settings_id)
        if not organization_user_settings:
            return None
        for field, value in organization_user_settings_in.dict(exclude_unset=True).items():
            setattr(organization_user_settings, field, value)
        return self.organization_user_settings_repo.update(organization_user_settings)

    def delete_organization_user_settings(self, organization_user_settings_id: str):
        self.organization_user_settings_repo.delete(organization_user_settings_id)
