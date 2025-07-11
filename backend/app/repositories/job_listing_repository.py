from sqlalchemy.orm import Session

from app.db.models.job_listing import JobListing


class JobListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, job_listing: JobListing) -> JobListing:
        self.db.add(job_listing)
        self.db.commit()
        self.db.refresh(job_listing)
        return job_listing

    def get_by_id(self, job_listing_id: str) -> JobListing:
        return self.db.query(JobListing).filter(JobListing.id == job_listing_id).first()

    def get_all(self) -> list[JobListing]:
        return self.db.query(JobListing).all()

    def update(self, job_listing: JobListing) -> JobListing:
        self.db.merge(job_listing)
        self.db.commit()
        self.db.refresh(job_listing)
        return job_listing

    def delete(self, job_listing_id: str):
        job_listing = self.db.query(JobListing).filter(JobListing.id == job_listing_id).first()
        if job_listing:
            self.db.delete(job_listing)
            self.db.commit()
