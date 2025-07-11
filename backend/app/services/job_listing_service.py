import uuid

from sqlalchemy.orm import Session

from app.db.models.job_listing import JobListing
from app.repositories.job_listing_repository import JobListingRepository
from app.schemas.job_listing import JobListingCreate, JobListingUpdate


class JobListingService:
    def __init__(self, db: Session):
        self.job_listing_repo = JobListingRepository(db)

    def create_job_listing(self, job_listing_in: JobListingCreate) -> JobListing:
        job_listing = JobListing(**job_listing_in.dict())
        job_listing.id = str(uuid.uuid4())
        return self.job_listing_repo.create(job_listing)

    def get_job_listing_by_id(self, job_listing_id: str) -> JobListing:
        return self.job_listing_repo.get_by_id(job_listing_id)

    def get_all_job_listings(self) -> list[JobListing]:
        return self.job_listing_repo.get_all()

    def update_job_listing(self, job_listing_id: str, job_listing_in: JobListingUpdate) -> JobListing:
        job_listing = self.job_listing_repo.get_by_id(job_listing_id)
        if not job_listing:
            return None
        for field, value in job_listing_in.dict(exclude_unset=True).items():
            setattr(job_listing, field, value)
        return self.job_listing_repo.update(job_listing)

    def delete_job_listing(self, job_listing_id: str):
        self.job_listing_repo.delete(job_listing_id)
