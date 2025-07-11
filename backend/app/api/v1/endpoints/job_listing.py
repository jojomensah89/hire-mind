from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job_listing import JobListingCreate, JobListingUpdate, JobListingResponse as JobListing
from app.services.job_listing_service import JobListingService

router = APIRouter()


@router.post("/job_listings", response_model=JobListing)
def create_job_listing(job_listing_in: JobListingCreate, db: Session = Depends(get_db)):
    service = JobListingService(db)
    return service.create_job_listing(job_listing_in)


@router.get("/job_listings/{job_listing_id}", response_model=JobListing)
def get_job_listing(job_listing_id: str, db: Session = Depends(get_db)):
    service = JobListingService(db)
    job_listing = service.get_job_listing_by_id(job_listing_id)
    if not job_listing:
        raise HTTPException(status_code=404, detail="Job Listing not found")
    return job_listing


@router.get("/job_listings", response_model=list[JobListing])
def get_all_job_listings(db: Session = Depends(get_db)):
    service = JobListingService(db)
    return service.get_all_job_listings()


@router.put("/job_listings/{job_listing_id}", response_model=JobListing)
def update_job_listing(job_listing_id: str, job_listing_in: JobListingUpdate, db: Session = Depends(get_db)):
    service = JobListingService(db)
    job_listing = service.update_job_listing(job_listing_id, job_listing_in)
    if not job_listing:
        raise HTTPException(status_code=404, detail="Job Listing not found")
    return job_listing


@router.delete("/job_listings/{job_listing_id}", status_code=204)
def delete_job_listing(job_listing_id: str, db: Session = Depends(get_db)):
    service = JobListingService(db)
    service.delete_job_listing(job_listing_id)
    return {"ok": True}
