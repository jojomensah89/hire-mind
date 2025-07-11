import uuid

from sqlalchemy.orm import Session

from app.db.models.organization import Organization
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationService:
    def __init__(self, db: Session):
        self.organization_repo = OrganizationRepository(db)

    def create_organization(self, organization_in: OrganizationCreate) -> Organization:
        organization = Organization(**organization_in.dict())
        organization.id = str(uuid.uuid4())
        return self.organization_repo.create(organization)

    def get_organization_by_id(self, organization_id: str) -> Organization:
        return self.organization_repo.get_by_id(organization_id)

    def get_all_organizations(self) -> list[Organization]:
        return self.organization_repo.get_all()

    def update_organization(self, organization_id: str, organization_in: OrganizationUpdate) -> Organization:
        organization = self.organization_repo.get_by_id(organization_id)
        if not organization:
            return None
        for field, value in organization_in.dict(exclude_unset=True).items():
            setattr(organization, field, value)
        return self.organization_repo.update(organization)

    def delete_organization(self, organization_id: str):
        self.organization_repo.delete(organization_id)
