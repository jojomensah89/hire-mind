from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional

from app.db.models.user import User
from app.exceptions.auth_exceptions import (
    DatabaseOperationError,
    UserNotFoundError,
    UserCreationError,
    UserUpdateError,
    UserDeletionError
)
from app.config.logging import get_auth_logger, log_auth_event

logger = get_auth_logger("user_repository")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Create a new user with comprehensive error handling"""
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            log_auth_event(
                logger,
                "user_created",
                f"Successfully created user in database",
                user_id=user.id,
                clerk_id=user.clerk_id
            )
            
            return user
            
        except IntegrityError as e:
            self.db.rollback()
            error_msg = f"User creation failed due to constraint violation"
            log_auth_event(
                logger,
                "user_creation_failed",
                error_msg,
                level="ERROR",
                clerk_id=getattr(user, 'clerk_id', None),
                error_details={"constraint_error": str(e.orig)}
            )
            raise UserCreationError(
                error_msg,
                details={"constraint_error": str(e.orig), "user_data": {"clerk_id": user.clerk_id}}
            )
            
        except SQLAlchemyError as e:
            self.db.rollback()
            error_msg = f"Database error during user creation"
            log_auth_event(
                logger,
                "user_creation_failed",
                error_msg,
                level="ERROR",
                clerk_id=getattr(user, 'clerk_id', None),
                error_details={"database_error": str(e)}
            )
            raise DatabaseOperationError(
                error_msg,
                details={"database_error": str(e), "operation": "create"}
            )

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID with error handling"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if user:
                log_auth_event(
                    logger,
                    "user_lookup_success",
                    f"Successfully found user by ID",
                    user_id=user_id,
                    clerk_id=user.clerk_id
                )
            else:
                log_auth_event(
                    logger,
                    "user_not_found",
                    f"User not found by ID",
                    level="WARNING",
                    user_id=user_id
                )
            
            return user
            
        except SQLAlchemyError as e:
            error_msg = f"Database error during user lookup by ID"
            log_auth_event(
                logger,
                "user_lookup_failed",
                error_msg,
                level="ERROR",
                user_id=user_id,
                error_details={"database_error": str(e)}
            )
            raise DatabaseOperationError(
                error_msg,
                details={"database_error": str(e), "operation": "get_by_id", "user_id": user_id}
            )

    def get_by_clerk_id(self, clerk_id: str) -> Optional[User]:
        """Get user by Clerk ID for webhook operations with error handling"""
        try:
            user = self.db.query(User).filter(User.clerk_id == clerk_id).first()
            
            if user:
                log_auth_event(
                    logger,
                    "user_lookup_success",
                    f"Successfully found user by Clerk ID",
                    user_id=user.id,
                    clerk_id=clerk_id
                )
            else:
                log_auth_event(
                    logger,
                    "user_not_found",
                    f"User not found by Clerk ID",
                    level="WARNING",
                    clerk_id=clerk_id
                )
            
            return user
            
        except SQLAlchemyError as e:
            error_msg = f"Database error during user lookup by Clerk ID"
            log_auth_event(
                logger,
                "user_lookup_failed",
                error_msg,
                level="ERROR",
                clerk_id=clerk_id,
                error_details={"database_error": str(e)}
            )
            raise DatabaseOperationError(
                error_msg,
                details={"database_error": str(e), "operation": "get_by_clerk_id", "clerk_id": clerk_id}
            )

    def get_all(self) -> list[User]:
        """Get all users with error handling"""
        try:
            users = self.db.query(User).all()
            
            log_auth_event(
                logger,
                "users_list_success",
                f"Successfully retrieved {len(users)} users"
            )
            
            return users
            
        except SQLAlchemyError as e:
            error_msg = f"Database error during user list retrieval"
            log_auth_event(
                logger,
                "users_list_failed",
                error_msg,
                level="ERROR",
                error_details={"database_error": str(e)}
            )
            raise DatabaseOperationError(
                error_msg,
                details={"database_error": str(e), "operation": "get_all"}
            )

    def update(self, user: User) -> User:
        """Update user with comprehensive error handling"""
        try:
            self.db.merge(user)
            self.db.commit()
            self.db.refresh(user)
            
            log_auth_event(
                logger,
                "user_updated",
                f"Successfully updated user in database",
                user_id=user.id,
                clerk_id=user.clerk_id
            )
            
            return user
            
        except IntegrityError as e:
            self.db.rollback()
            error_msg = f"User update failed due to constraint violation"
            log_auth_event(
                logger,
                "user_update_failed",
                error_msg,
                level="ERROR",
                user_id=user.id,
                clerk_id=user.clerk_id,
                error_details={"constraint_error": str(e.orig)}
            )
            raise UserUpdateError(
                error_msg,
                details={"constraint_error": str(e.orig), "user_id": user.id}
            )
            
        except SQLAlchemyError as e:
            self.db.rollback()
            error_msg = f"Database error during user update"
            log_auth_event(
                logger,
                "user_update_failed",
                error_msg,
                level="ERROR",
                user_id=user.id,
                clerk_id=getattr(user, 'clerk_id', None),
                error_details={"database_error": str(e)}
            )
            raise DatabaseOperationError(
                error_msg,
                details={"database_error": str(e), "operation": "update", "user_id": user.id}
            )

    def delete(self, user_id: str) -> bool:
        """Delete user with comprehensive error handling"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if not user:
                log_auth_event(
                    logger,
                    "user_delete_failed",
                    f"Cannot delete user - user not found",
                    level="WARNING",
                    user_id=user_id
                )
                raise UserNotFoundError(
                    f"User not found for deletion",
                    details={"user_id": user_id}
                )
            
            clerk_id = user.clerk_id
            self.db.delete(user)
            self.db.commit()
            
            log_auth_event(
                logger,
                "user_deleted",
                f"Successfully deleted user from database",
                user_id=user_id,
                clerk_id=clerk_id
            )
            
            return True
            
        except UserNotFoundError:
            # Re-raise user not found errors
            raise
            
        except SQLAlchemyError as e:
            self.db.rollback()
            error_msg = f"Database error during user deletion"
            log_auth_event(
                logger,
                "user_delete_failed",
                error_msg,
                level="ERROR",
                user_id=user_id,
                error_details={"database_error": str(e)}
            )
            raise DatabaseOperationError(
                error_msg,
                details={"database_error": str(e), "operation": "delete", "user_id": user_id}
            )
