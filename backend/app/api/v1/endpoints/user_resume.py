from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user_resume import UserResumeCreate, UserResumeUpdate, UserResumeResponse as UserResume
from app.services.user_resume_service import UserResumeService

router = APIRouter()


@router.post("/user_resumes", response_model=UserResume)
def create_user_resume(user_resume_in: UserResumeCreate, db: Session = Depends(get_db)):
    service = UserResumeService(db)
    return service.create_user_resume(user_resume_in)


@router.get("/user_resumes/{user_resume_id}", response_model=UserResume)
def get_user_resume(user_resume_id: str, db: Session = Depends(get_db)):
    service = UserResumeService(db)
    user_resume = service.get_user_resume_by_id(user_resume_id)
    if not user_resume:
        raise HTTPException(status_code=404, detail="User Resume not found")
    return user_resume


@router.get("/user_resumes", response_model=list[UserResume])
def get_all_user_resumes(db: Session = Depends(get_db)):
    service = UserResumeService(db)
    return service.get_all_user_resumes()


@router.put("/user_resumes/{user_resume_id}", response_model=UserResume)
def update_user_resume(user_resume_id: str, user_resume_in: UserResumeUpdate, db: Session = Depends(get_db)):
    service = UserResumeService(db)
    user_resume = service.update_user_resume(user_resume_id, user_resume_in)
    if not user_resume:
        raise HTTPException(status_code=404, detail="User Resume not found")
    return user_resume


@router.delete("/user_resumes/{user_resume_id}", status_code=204)
def delete_user_resume(user_resume_id: str, db: Session = Depends(get_db)):
    service = UserResumeService(db)
    service.delete_user_resume(user_resume_id)
    return {"ok": True}
