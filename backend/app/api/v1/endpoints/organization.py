from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse as Organization
from app.services.organization_service import OrganizationService

router = APIRouter()


@router.post("/organizations", response_model=Organization)
def create_organization(organization_in: OrganizationCreate, db: Session = Depends(get_db)):
    service = OrganizationService(db)
    return service.create_organization(organization_in)


@router.get("/organizations/{organization_id}", response_model=Organization)
def get_organization(organization_id: str, db: Session = Depends(get_db)):
    service = OrganizationService(db)
    organization = service.get_organization_by_id(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.get("/organizations", response_model=list[Organization])
def get_all_organizations(db: Session = Depends(get_db)):
    service = OrganizationService(db)
    return service.get_all_organizations()


@router.put("/organizations/{organization_id}", response_model=Organization)
def update_organization(organization_id: str, organization_in: OrganizationUpdate, db: Session = Depends(get_db)):
    service = OrganizationService(db)
    organization = service.update_organization(organization_id, organization_in)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.delete("/organizations/{organization_id}", status_code=204)
def delete_organization(organization_id: str, db: Session = Depends(get_db)):
    service = OrganizationService(db)
    service.delete_organization(organization_id)
    return {"ok": True}
