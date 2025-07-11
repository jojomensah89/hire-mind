from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job_listing_application import JobListingApplicationCreate, JobListingApplicationUpdate, \
    JobListingApplicationResponse as JobListingApplication
from app.services.job_listing_application_service import JobListingApplicationService

router = APIRouter()


@router.post("/job_listing_applications", response_model=JobListingApplication)
def create_job_listing_application(job_listing_application_in: JobListingApplicationCreate,
                                   db: Session = Depends(get_db)):
    service = JobListingApplicationService(db)
    return service.create_job_listing_application(job_listing_application_in)


@router.get("/job_listing_applications/{job_listing_application_id}", response_model=JobListingApplication)
def get_job_listing_application(job_listing_application_id: str, db: Session = Depends(get_db)):
    service = JobListingApplicationService(db)
    job_listing_application = service.get_job_listing_application_by_id(job_listing_application_id)
    if not job_listing_application:
        raise HTTPException(status_code=404, detail="Job Listing Application not found")
    return job_listing_application


@router.get("/job_listing_applications", response_model=list[JobListingApplication])
def get_all_job_listing_applications(db: Session = Depends(get_db)):
    service = JobListingApplicationService(db)
    return service.get_all_job_listing_applications()


@router.put("/job_listing_applications/{job_listing_application_id}", response_model=JobListingApplication)
def update_job_listing_application(job_listing_application_id: str,
                                   job_listing_application_in: JobListingApplicationUpdate,
                                   db: Session = Depends(get_db)):
    service = JobListingApplicationService(db)
    job_listing_application = service.update_job_listing_application(job_listing_application_id,
                                                                     job_listing_application_in)
    if not job_listing_application:
        raise HTTPException(status_code=404, detail="Job Listing Application not found")
    return job_listing_application


@router.delete("/job_listing_applications/{job_listing_application_id}", status_code=204)
def delete_job_listing_application(job_listing_application_id: str, db: Session = Depends(get_db)):
    service = JobListingApplicationService(db)
    service.delete_job_listing_application(job_listing_application_id)
    return {"ok": True}
