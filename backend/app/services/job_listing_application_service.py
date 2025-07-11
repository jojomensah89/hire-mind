import uuid

from sqlalchemy.orm import Session

from app.db.models.job_listing_application import JobListingApplication
from app.repositories.job_listing_application_repository import JobListingApplicationRepository
from app.schemas.job_listing_application import JobListingApplicationCreate, JobListingApplicationUpdate


class JobListingApplicationService:
    def __init__(self, db: Session):
        self.job_listing_application_repo = JobListingApplicationRepository(db)

    def create_job_listing_application(self,
                                       job_listing_application_in: JobListingApplicationCreate) -> JobListingApplication:
        job_listing_application = JobListingApplication(**job_listing_application_in.dict())
        job_listing_application.id = str(uuid.uuid4())
        return self.job_listing_application_repo.create(job_listing_application)

    def get_job_listing_application_by_id(self, job_listing_application_id: str) -> JobListingApplication:
        return self.job_listing_application_repo.get_by_id(job_listing_application_id)

    def get_all_job_listing_applications(self) -> list[JobListingApplication]:
        return self.job_listing_application_repo.get_all()

    def update_job_listing_application(self, job_listing_application_id: str,
                                       job_listing_application_in: JobListingApplicationUpdate) -> JobListingApplication:
        job_listing_application = self.job_listing_application_repo.get_by_id(job_listing_application_id)
        if not job_listing_application:
            return None
        for field, value in job_listing_application_in.dict(exclude_unset=True).items():
            setattr(job_listing_application, field, value)
        return self.job_listing_application_repo.update(job_listing_application)

    def delete_job_listing_application(self, job_listing_application_id: str):
        self.job_listing_application_repo.delete(job_listing_application_id)
