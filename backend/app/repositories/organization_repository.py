from sqlalchemy.orm import Session

from app.db.models.organization import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, organization: Organization) -> Organization:
        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def get_by_id(self, organization_id: str) -> Organization:
        return self.db.query(Organization).filter(Organization.id == organization_id).first()

    def get_all(self) -> list[Organization]:
        return self.db.query(Organization).all()

    def update(self, organization: Organization) -> Organization:
        self.db.merge(organization)
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def delete(self, organization_id: str):
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        if organization:
            self.db.delete(organization)
            self.db.commit()
