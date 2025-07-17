from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.clerk.clerk_dependencies import (
    require_clerk_auth,
    get_current_user_id,
)
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_clerk_auth)])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # This endpoint should ideally be restricted to admins.
    # For now, any authenticated user can create a new user.
    user_service = UserService(db)
    user = user_service.create_user(user_in)
    return user


@router.get("/", response_model=list[UserResponse], dependencies=[Depends(require_clerk_auth)])
def get_all_users(db: Session = Depends(get_db)):
    # This endpoint should ideally be restricted to admins.
    # For now, any authenticated user can get all users.
    user_service = UserService(db)
    users = user_service.get_all_users()
    return users


@router.get("/me", response_model=UserResponse, dependencies=[Depends(require_clerk_auth)])
def get_me(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/me", response_model=UserResponse, dependencies=[Depends(require_clerk_auth)])
def update_me(user_in: UserUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    user_service = UserService(db)
    user = user_service.update_user(user_id, user_in)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_clerk_auth)])
def delete_me(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_service.delete_user(user_id)
    return


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_clerk_auth)])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    # This endpoint should ideally be restricted to admins.
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
