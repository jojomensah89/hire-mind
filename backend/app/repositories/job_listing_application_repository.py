from sqlalchemy.orm import Session

from app.db.models.job_listing_application import JobListingApplication


class JobListingApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job_listing_application: JobListingApplication) -> JobListingApplication:
        self.db.add(job_listing_application)
        self.db.commit()
        self.db.refresh(job_listing_application)
        return job_listing_application

    def get_by_id(self, job_listing_application_id: str) -> JobListingApplication:
        return self.db.query(JobListingApplication).filter(
            JobListingApplication.id == job_listing_application_id).first()

    def get_all(self) -> list[JobListingApplication]:
        return self.db.query(JobListingApplication).all()

    def update(self, job_listing_application: JobListingApplication) -> JobListingApplication:
        self.db.merge(job_listing_application)
        self.db.commit()
        self.db.refresh(job_listing_application)
        return job_listing_application

    def delete(self, job_listing_application_id: str):
        job_listing_application = self.db.query(JobListingApplication).filter(
            JobListingApplication.id == job_listing_application_id).first()
        if job_listing_application:
            self.db.delete(job_listing_application)
            self.db.commit()
