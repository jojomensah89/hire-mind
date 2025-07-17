import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions.auth_exceptions import (
    UserNotFoundError,
    UserCreationError,
    UserUpdateError,
    UserDeletionError,
    WebhookPayloadError
)
from app.config.logging import get_auth_logger, log_auth_event

logger = get_auth_logger("user_service")


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        """Create a new user with error handling"""
        try:
            user = User(
                id=str(uuid.uuid4()),
                **user_in.dict()
            )
            return self.user_repo.create(user)
        except Exception as e:
            log_auth_event(
                logger,
                "user_service_create_failed",
                f"User service failed to create user",
                level="ERROR",
                clerk_id=user_in.clerk_id,
                error_details={"service_error": str(e)}
            )
            raise

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID with error handling"""
        try:
            return self.user_repo.get_by_id(user_id)
        except Exception as e:
            log_auth_event(
                logger,
                "user_service_get_failed",
                f"User service failed to get user by ID",
                level="ERROR",
                user_id=user_id,
                error_details={"service_error": str(e)}
            )
            raise

    def get_user_by_clerk_id(self, clerk_id: str) -> Optional[User]:
        """Get user by Clerk ID with error handling"""
        try:
            return self.user_repo.get_by_clerk_id(clerk_id)
        except Exception as e:
            log_auth_event(
                logger,
                "user_service_get_failed",
                f"User service failed to get user by Clerk ID",
                level="ERROR",
                clerk_id=clerk_id,
                error_details={"service_error": str(e)}
            )
            raise

    def get_all_users(self) -> list[User]:
        """Get all users with error handling"""
        try:
            return self.user_repo.get_all()
        except Exception as e:
            log_auth_event(
                logger,
                "user_service_list_failed",
                f"User service failed to get all users",
                level="ERROR",
                error_details={"service_error": str(e)}
            )
            raise

    def update_user(self, user_id: str, user_in: UserUpdate) -> Optional[User]:
        """Update user with comprehensive error handling"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                log_auth_event(
                    logger,
                    "user_service_update_failed",
                    f"Cannot update user - user not found",
                    level="WARNING",
                    user_id=user_id
                )
                raise UserNotFoundError(
                    f"User not found for update",
                    details={"user_id": user_id}
                )
            
            for field, value in user_in.dict(exclude_unset=True).items():
                setattr(user, field, value)
            
            return self.user_repo.update(user)
            
        except UserNotFoundError:
            # Re-raise user not found errors
            raise
        except Exception as e:
            log_auth_event(
                logger,
                "user_service_update_failed",
                f"User service failed to update user",
                level="ERROR",
                user_id=user_id,
                error_details={"service_error": str(e)}
            )
            raise

    def delete_user(self, user_id: str) -> bool:
        """Delete user with error handling"""
        try:
            return self.user_repo.delete(user_id)
        except Exception as e:
            log_auth_event(
                logger,
                "user_service_delete_failed",
                f"User service failed to delete user",
                level="ERROR",
                user_id=user_id,
                error_details={"service_error": str(e)}
            )
            raise

    def create_user_from_webhook(self, user_data: dict) -> User:
        """Create user from webhook data with comprehensive error handling and validation"""
        try:
            # Validate required fields
            clerk_id = user_data.get('id')
            if not clerk_id:
                raise WebhookPayloadError(
                    "Missing required field 'id' in webhook user data",
                    details={"user_data": user_data}
                )
            
            log_auth_event(
                logger,
                "webhook_user_creation_started",
                f"Starting user creation from webhook",
                clerk_id=clerk_id,
                event_data={"user_data_keys": list(user_data.keys())}
            )
            
            # Safely extract email from email_addresses array
            email_addresses = user_data.get('email_addresses', [])
            email = None
            if email_addresses and isinstance(email_addresses, list) and len(email_addresses) > 0:
                if isinstance(email_addresses[0], dict):
                    email = email_addresses[0].get('email_address')
            
            # Safely extract phone number from phone_numbers array
            phone_numbers = user_data.get('phone_numbers', [])
            phone_number = None
            if phone_numbers and isinstance(phone_numbers, list) and len(phone_numbers) > 0:
                if isinstance(phone_numbers[0], dict):
                    phone_number = phone_numbers[0].get('phone_number')
            
            user_in = UserCreate(
                clerk_id=clerk_id,
                email=email,
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                phone_number=phone_number,
                image_url=user_data.get('image_url'),
            )
            
            user = self.create_user(user_in)
            
            log_auth_event(
                logger,
                "webhook_user_creation_success",
                f"Successfully created user from webhook",
                user_id=user.id,
                clerk_id=clerk_id
            )
            
            return user
            
        except WebhookPayloadError:
            # Re-raise payload errors
            raise
        except Exception as e:
            log_auth_event(
                logger,
                "webhook_user_creation_failed",
                f"Failed to create user from webhook",
                level="ERROR",
                clerk_id=user_data.get('id'),
                error_details={"service_error": str(e), "user_data": user_data}
            )
            raise UserCreationError(
                f"Failed to create user from webhook data",
                details={"webhook_error": str(e), "clerk_id": user_data.get('id')}
            )

    def update_user_from_webhook(self, user_data: dict) -> Optional[User]:
        """Update user from webhook data with comprehensive error handling and validation"""
        try:
            # Validate required fields
            clerk_id = user_data.get('id')
            if not clerk_id:
                raise WebhookPayloadError(
                    "Missing required field 'id' in webhook user data",
                    details={"user_data": user_data}
                )
            
            log_auth_event(
                logger,
                "webhook_user_update_started",
                f"Starting user update from webhook",
                clerk_id=clerk_id,
                event_data={"user_data_keys": list(user_data.keys())}
            )
            
            user = self.user_repo.get_by_clerk_id(clerk_id)
            if not user:
                log_auth_event(
                    logger,
                    "webhook_user_update_failed",
                    f"Cannot update user from webhook - user not found",
                    level="WARNING",
                    clerk_id=clerk_id
                )
                raise UserNotFoundError(
                    f"User not found for webhook update",
                    details={"clerk_id": clerk_id}
                )

            # Safely extract email from email_addresses array
            email_addresses = user_data.get('email_addresses', [])
            email = None
            if email_addresses and isinstance(email_addresses, list) and len(email_addresses) > 0:
                if isinstance(email_addresses[0], dict):
                    email = email_addresses[0].get('email_address')
            
            # Safely extract phone number from phone_numbers array
            phone_numbers = user_data.get('phone_numbers', [])
            phone_number = None
            if phone_numbers and isinstance(phone_numbers, list) and len(phone_numbers) > 0:
                if isinstance(phone_numbers[0], dict):
                    phone_number = phone_numbers[0].get('phone_number')

            user_in = UserUpdate(
                email=email,
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                phone_number=phone_number,
                image_url=user_data.get('image_url'),
            )
            
            updated_user = self.update_user(user.id, user_in)
            
            log_auth_event(
                logger,
                "webhook_user_update_success",
                f"Successfully updated user from webhook",
                user_id=user.id,
                clerk_id=clerk_id
            )
            
            return updated_user
            
        except (WebhookPayloadError, UserNotFoundError):
            # Re-raise specific errors
            raise
        except Exception as e:
            log_auth_event(
                logger,
                "webhook_user_update_failed",
                f"Failed to update user from webhook",
                level="ERROR",
                clerk_id=user_data.get('id'),
                error_details={"service_error": str(e), "user_data": user_data}
            )
            raise UserUpdateError(
                f"Failed to update user from webhook data",
                details={"webhook_error": str(e), "clerk_id": user_data.get('id')}
            )

    def delete_user_from_webhook(self, user_data: dict) -> bool:
        """Delete user from webhook data with comprehensive error handling and validation"""
        try:
            # Validate required fields
            clerk_id = user_data.get('id')
            if not clerk_id:
                raise WebhookPayloadError(
                    "Missing required field 'id' in webhook user data",
                    details={"user_data": user_data}
                )
            
            log_auth_event(
                logger,
                "webhook_user_deletion_started",
                f"Starting user deletion from webhook",
                clerk_id=clerk_id
            )
            
            user = self.user_repo.get_by_clerk_id(clerk_id)
            if not user:
                log_auth_event(
                    logger,
                    "webhook_user_deletion_skipped",
                    f"User not found for webhook deletion - skipping",
                    level="WARNING",
                    clerk_id=clerk_id
                )
                # For deletion, we don't raise an error if user doesn't exist
                # This handles the case where the user was already deleted
                return False
            
            result = self.delete_user(user.id)
            
            log_auth_event(
                logger,
                "webhook_user_deletion_success",
                f"Successfully deleted user from webhook",
                user_id=user.id,
                clerk_id=clerk_id
            )
            
            return result
            
        except WebhookPayloadError:
            # Re-raise payload errors
            raise
        except Exception as e:
            log_auth_event(
                logger,
                "webhook_user_deletion_failed",
                f"Failed to delete user from webhook",
                level="ERROR",
                clerk_id=user_data.get('id'),
                error_details={"service_error": str(e), "user_data": user_data}
            )
            raise UserDeletionError(
                f"Failed to delete user from webhook data",
                details={"webhook_error": str(e), "clerk_id": user_data.get('id')}
            )
