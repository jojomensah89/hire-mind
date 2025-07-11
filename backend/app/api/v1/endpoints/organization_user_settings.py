from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.organization_user_settings import OrganizationUserSettingsCreate, OrganizationUserSettingsUpdate, \
    OrganizationUserSettingsResponse as OrganizationUserSettings
from app.services.organization_user_settings_service import OrganizationUserSettingsService

router = APIRouter()


@router.post("/organization_user_settings", response_model=OrganizationUserSettings)
def create_organization_user_settings(organization_user_settings_in: OrganizationUserSettingsCreate,
                                      db: Session = Depends(get_db)):
    service = OrganizationUserSettingsService(db)
    return service.create_organization_user_settings(organization_user_settings_in)


@router.get("/organization_user_settings/{organization_user_settings_id}", response_model=OrganizationUserSettings)
def get_organization_user_settings(organization_user_settings_id: str, db: Session = Depends(get_db)):
    service = OrganizationUserSettingsService(db)
    organization_user_settings = service.get_organization_user_settings_by_id(organization_user_settings_id)
    if not organization_user_settings:
        raise HTTPException(status_code=404, detail="Organization User Settings not found")
    return organization_user_settings


@router.get("/organization_user_settings", response_model=list[OrganizationUserSettings])
def get_all_organization_user_settings(db: Session = Depends(get_db)):
    service = OrganizationUserSettingsService(db)
    return service.get_all_organization_user_settings()


@router.put("/organization_user_settings/{organization_user_settings_id}", response_model=OrganizationUserSettings)
def update_organization_user_settings(organization_user_settings_id: str,
                                      organization_user_settings_in: OrganizationUserSettingsUpdate,
                                      db: Session = Depends(get_db)):
    service = OrganizationUserSettingsService(db)
    organization_user_settings = service.update_organization_user_settings(organization_user_settings_id,
                                                                           organization_user_settings_in)
    if not organization_user_settings:
        raise HTTPException(status_code=404, detail="Organization User Settings not found")
    return organization_user_settings


@router.delete("/organization_user_settings/{organization_user_settings_id}", status_code=204)
def delete_organization_user_settings(organization_user_settings_id: str, db: Session = Depends(get_db)):
    service = OrganizationUserSettingsService(db)
    service.delete_organization_user_settings(organization_user_settings_id)
    return {"ok": True}
