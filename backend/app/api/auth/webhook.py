import hmac
import hashlib
import json
import time
from typing import Dict, Any, Callable, Awaitable
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.config.settings import settings
from svix.webhooks import Webhook, WebhookVerificationError
from app.exceptions.auth_exceptions import (
    WebhookSignatureError,
    WebhookTimestampError,
    WebhookPayloadError,
    UserNotFoundError,
    UserCreationError,
    UserUpdateError,
    UserDeletionError,
    DatabaseOperationError,
    ConfigurationError
)
from app.config.logging import get_auth_logger, log_auth_event

logger = get_auth_logger("webhook")

router = APIRouter(tags=["auth"])


class ClerkWebhookHandler:
    """Handler for Clerk webhook events"""

    def __init__(self, webhook_secret: str):
        self.webhook_secret = webhook_secret
        self.event_handlers: Dict[str, Callable[[Dict[str, Any], Session], Awaitable[None]]] = {
            "user.created": self.handle_user_created,
            "user.updated": self.handle_user_updated,
            "user.deleted": self.handle_user_deleted,
        }

    def verify_webhook_signature(self, payload: bytes, headers: Dict[str, str]) -> None:
        """Verify webhook signature from Clerk/Svix with comprehensive error handling"""
        import os
        env = os.getenv("ENV", "development")
        
        log_auth_event(
            logger,
            "webhook_signature_verification_started",
            "Starting webhook signature verification",
            event_data={"environment": env, "has_secret": bool(self.webhook_secret)}
        )
        
        if not self.webhook_secret:
            error_msg = "Webhook signature verification failed - no secret configured"
            log_auth_event(
                logger,
                "webhook_signature_verification_failed",
                error_msg,
                level="ERROR",
                error_details={"reason": "missing_secret", "environment": env}
            )
            if env == "development":
                log_auth_event(
                    logger,
                    "webhook_signature_verification_skipped",
                    "Skipping signature verification in development mode",
                    level="WARNING"
                )
                return
            raise ConfigurationError(
                error_msg,
                details={"environment": env, "required_setting": "CLERK_WEBHOOK_SECRET"}
            )

        # Extract Svix headers
        svix_signature = headers.get('svix-signature', '')
        svix_timestamp = headers.get('svix-timestamp', '')
        svix_id = headers.get('svix-id', '')

        log_auth_event(
            logger,
            "webhook_headers_extracted",
            "Extracted webhook headers for verification",
            event_data={
                "has_signature": bool(svix_signature),
                "has_timestamp": bool(svix_timestamp),
                "has_id": bool(svix_id),
                "signature_preview": svix_signature[:20] + "..." if len(svix_signature) > 20 else svix_signature
            }
        )

        if not all([svix_signature, svix_timestamp, svix_id]):
            missing_headers = [
                header for header, value in [
                    ("svix-signature", svix_signature),
                    ("svix-timestamp", svix_timestamp),
                    ("svix-id", svix_id)
                ] if not value
            ]
            
            error_msg = f"Missing required Svix headers: {', '.join(missing_headers)}"
            log_auth_event(
                logger,
                "webhook_signature_verification_failed",
                error_msg,
                level="ERROR",
                error_details={"missing_headers": missing_headers}
            )
            raise WebhookSignatureError(
                error_msg,
                details={"missing_headers": missing_headers, "provided_headers": list(headers.keys())}
            )

        try:
            # Validate timestamp to prevent replay attacks (5 minute tolerance)
            current_time = int(time.time())
            try:
                webhook_timestamp = int(svix_timestamp)
            except ValueError as e:
                error_msg = f"Invalid timestamp format in webhook headers: {svix_timestamp}"
                log_auth_event(
                    logger,
                    "webhook_timestamp_validation_failed",
                    error_msg,
                    level="ERROR",
                    error_details={"svix_timestamp": svix_timestamp, "parse_error": str(e)}
                )
                raise WebhookTimestampError(
                    error_msg,
                    details={"svix_timestamp": svix_timestamp, "parse_error": str(e)}
                )
            
            time_diff = abs(current_time - webhook_timestamp)
            
            # 5 minute tolerance (300 seconds)
            if time_diff > 300:
                error_msg = f"Webhook timestamp outside acceptable range (diff: {time_diff}s)"
                log_auth_event(
                    logger,
                    "webhook_timestamp_validation_failed",
                    error_msg,
                    level="ERROR",
                    error_details={
                        "current_time": current_time,
                        "webhook_timestamp": webhook_timestamp,
                        "time_diff_seconds": time_diff,
                        "max_allowed_seconds": 300
                    }
                )
                raise WebhookTimestampError(
                    error_msg,
                    details={
                        "current_time": current_time,
                        "webhook_timestamp": webhook_timestamp,
                        "time_diff_seconds": time_diff,
                        "max_allowed_seconds": 300
                    }
                )

            # Use Svix library for signature verification
            webhook = Webhook(self.webhook_secret)
            
            # Prepare headers dict for Svix verification
            svix_headers = {
                "svix-signature": svix_signature,
                "svix-timestamp": svix_timestamp,
                "svix-id": svix_id
            }
            
            # Verify the webhook signature
            webhook.verify(payload, svix_headers)
            
            log_auth_event(
                logger,
                "webhook_signature_verification_success",
                "Webhook signature verification successful",
                event_data={"timestamp_diff": time_diff}
            )

        except WebhookVerificationError as e:
            error_msg = f"Svix webhook signature verification failed: {str(e)}"
            log_auth_event(
                logger,
                "webhook_signature_verification_failed",
                error_msg,
                level="ERROR",
                error_details={
                    "svix_error": str(e),
                    "timestamp_diff": time_diff if 'time_diff' in locals() else None
                }
            )
            raise WebhookSignatureError(
                error_msg,
                details={"svix_error": str(e), "verification_method": "svix_library"}
            )

        except (WebhookTimestampError, WebhookSignatureError):
            # Re-raise our custom exceptions
            raise

        except Exception as e:
            error_msg = f"Unexpected error during webhook signature verification: {str(e)}"
            log_auth_event(
                logger,
                "webhook_signature_verification_failed",
                error_msg,
                level="ERROR",
                error_details={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            raise WebhookSignatureError(
                error_msg,
                details={"unexpected_error": str(e), "error_type": type(e).__name__}
            )

    async def handle_event(self, event_data: Dict[str, Any], db: Session):
        """Handle a webhook event by dispatching it to the appropriate handler with comprehensive error handling"""
        event_type = event_data.get("type")
        event_id = event_data.get("id", "unknown")
        
        if not event_type:
            error_msg = "Webhook event missing required 'type' field"
            log_auth_event(
                logger,
                "webhook_event_validation_failed",
                error_msg,
                level="ERROR",
                error_details={"event_data": event_data}
            )
            raise WebhookPayloadError(
                error_msg,
                details={"event_data": event_data}
            )
        
        log_auth_event(
            logger,
            "webhook_event_received",
            f"Received webhook event: {event_type}",
            event_data={
                "event_type": event_type,
                "event_id": event_id,
                "has_data": "data" in event_data
            }
        )
        
        handler = self.event_handlers.get(event_type)
        if handler:
            try:
                await handler(event_data, db)
                log_auth_event(
                    logger,
                    "webhook_event_handled_success",
                    f"Successfully handled event: {event_type}",
                    event_data={"event_type": event_type, "event_id": event_id}
                )
            except (UserCreationError, UserUpdateError, UserDeletionError, UserNotFoundError, WebhookPayloadError) as e:
                # Re-raise specific authentication errors
                log_auth_event(
                    logger,
                    "webhook_event_handled_failed",
                    f"Authentication error handling event {event_type}: {str(e)}",
                    level="ERROR",
                    event_data={"event_type": event_type, "event_id": event_id},
                    error_details={"auth_error": str(e), "error_type": type(e).__name__}
                )
                raise
            except DatabaseOperationError as e:
                # Re-raise database errors
                log_auth_event(
                    logger,
                    "webhook_event_handled_failed",
                    f"Database error handling event {event_type}: {str(e)}",
                    level="ERROR",
                    event_data={"event_type": event_type, "event_id": event_id},
                    error_details={"database_error": str(e)}
                )
                raise
            except Exception as e:
                error_msg = f"Unexpected error handling event {event_type}: {str(e)}"
                log_auth_event(
                    logger,
                    "webhook_event_handled_failed",
                    error_msg,
                    level="ERROR",
                    event_data={"event_type": event_type, "event_id": event_id},
                    error_details={"unexpected_error": str(e), "error_type": type(e).__name__}
                )
                raise DatabaseOperationError(
                    error_msg,
                    details={"unexpected_error": str(e), "event_type": event_type, "event_id": event_id}
                )
        else:
            log_auth_event(
                logger,
                "webhook_event_unhandled",
                f"Unhandled webhook event type: {event_type}",
                level="WARNING",
                event_data={"event_type": event_type, "event_id": event_id, "available_handlers": list(self.event_handlers.keys())}
            )

    async def handle_user_created(self, event_data: Dict[str, Any], db: Session):
        """Handle user.created event with comprehensive error handling and idempotency"""
        clerk_user = event_data.get('data', {})
        clerk_id = clerk_user.get('id')
        
        if not clerk_id:
            error_msg = "Received user.created event without Clerk ID"
            log_auth_event(
                logger,
                "webhook_user_created_validation_failed",
                error_msg,
                level="ERROR",
                error_details={"event_data": event_data}
            )
            raise WebhookPayloadError(
                error_msg,
                details={"event_data": event_data, "missing_field": "id"}
            )
        
        log_auth_event(
            logger,
            "webhook_user_created_started",
            f"Processing user.created event",
            clerk_id=clerk_id,
            event_data={"clerk_user_keys": list(clerk_user.keys())}
        )
        
        try:
            user_service = UserService(db)
            
            # Check if user already exists (idempotency)
            existing_user = user_service.get_user_by_clerk_id(clerk_id)
            if existing_user:
                log_auth_event(
                    logger,
                    "webhook_user_created_skipped",
                    f"User already exists, skipping creation (idempotent)",
                    user_id=existing_user.id,
                    clerk_id=clerk_id
                )
                return
            
            # Create new user
            user = user_service.create_user_from_webhook(clerk_user)
            log_auth_event(
                logger,
                "webhook_user_created_success",
                f"Successfully created user from webhook",
                user_id=user.id,
                clerk_id=user.clerk_id
            )
            
        except (UserCreationError, WebhookPayloadError, DatabaseOperationError) as e:
            # Re-raise specific errors
            raise
        except Exception as e:
            error_msg = f"Unexpected error in user.created handler: {str(e)}"
            log_auth_event(
                logger,
                "webhook_user_created_failed",
                error_msg,
                level="ERROR",
                clerk_id=clerk_id,
                error_details={"unexpected_error": str(e), "error_type": type(e).__name__}
            )
            raise UserCreationError(
                error_msg,
                details={"unexpected_error": str(e), "clerk_id": clerk_id}
            )

    async def handle_user_updated(self, event_data: Dict[str, Any], db: Session):
        """Handle user.updated event with comprehensive error handling"""
        clerk_user = event_data.get('data', {})
        clerk_id = clerk_user.get('id')
        
        if not clerk_id:
            error_msg = "Received user.updated event without Clerk ID"
            log_auth_event(
                logger,
                "webhook_user_updated_validation_failed",
                error_msg,
                level="ERROR",
                error_details={"event_data": event_data}
            )
            raise WebhookPayloadError(
                error_msg,
                details={"event_data": event_data, "missing_field": "id"}
            )
        
        log_auth_event(
            logger,
            "webhook_user_updated_started",
            f"Processing user.updated event",
            clerk_id=clerk_id,
            event_data={"clerk_user_keys": list(clerk_user.keys())}
        )
        
        try:
            user_service = UserService(db)
            updated_user = user_service.update_user_from_webhook(clerk_user)
            
            if updated_user:
                log_auth_event(
                    logger,
                    "webhook_user_updated_success",
                    f"Successfully updated user from webhook",
                    user_id=updated_user.id,
                    clerk_id=updated_user.clerk_id
                )
            else:
                # This case is handled by the service layer now
                pass
                
        except (UserUpdateError, UserNotFoundError, WebhookPayloadError, DatabaseOperationError) as e:
            # Re-raise specific errors
            raise
        except Exception as e:
            error_msg = f"Unexpected error in user.updated handler: {str(e)}"
            log_auth_event(
                logger,
                "webhook_user_updated_failed",
                error_msg,
                level="ERROR",
                clerk_id=clerk_id,
                error_details={"unexpected_error": str(e), "error_type": type(e).__name__}
            )
            raise UserUpdateError(
                error_msg,
                details={"unexpected_error": str(e), "clerk_id": clerk_id}
            )

    async def handle_user_deleted(self, event_data: Dict[str, Any], db: Session):
        """Handle user.deleted event with comprehensive error handling"""
        clerk_user = event_data.get('data', {})
        clerk_id = clerk_user.get('id')
        
        if not clerk_id:
            error_msg = "Received user.deleted event without Clerk ID"
            log_auth_event(
                logger,
                "webhook_user_deleted_validation_failed",
                error_msg,
                level="ERROR",
                error_details={"event_data": event_data}
            )
            raise WebhookPayloadError(
                error_msg,
                details={"event_data": event_data, "missing_field": "id"}
            )
        
        log_auth_event(
            logger,
            "webhook_user_deleted_started",
            f"Processing user.deleted event",
            clerk_id=clerk_id
        )
        
        try:
            user_service = UserService(db)
            
            # The service layer handles the case where user doesn't exist
            result = user_service.delete_user_from_webhook(clerk_user)
            
            if result:
                log_auth_event(
                    logger,
                    "webhook_user_deleted_success",
                    f"Successfully deleted user from webhook",
                    clerk_id=clerk_id
                )
            else:
                log_auth_event(
                    logger,
                    "webhook_user_deleted_skipped",
                    f"User not found for deletion - already deleted or never existed",
                    level="WARNING",
                    clerk_id=clerk_id
                )
                
        except (UserDeletionError, WebhookPayloadError, DatabaseOperationError) as e:
            # Re-raise specific errors
            raise
        except Exception as e:
            error_msg = f"Unexpected error in user.deleted handler: {str(e)}"
            log_auth_event(
                logger,
                "webhook_user_deleted_failed",
                error_msg,
                level="ERROR",
                clerk_id=clerk_id,
                error_details={"unexpected_error": str(e), "error_type": type(e).__name__}
            )
            raise UserDeletionError(
                error_msg,
                details={"unexpected_error": str(e), "clerk_id": clerk_id}
            )


webhook_handler = ClerkWebhookHandler(settings.CLERK_WEBHOOK_SECRET)


@router.post("/clerk")
async def clerk_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Clerk webhook events with comprehensive error handling and proper HTTP status codes"""
    request_id = id(request)  # Simple request ID for tracking
    
    log_auth_event(
        logger,
        "webhook_request_received",
        "Received webhook request",
        event_data={"request_id": request_id, "method": request.method, "url": str(request.url)}
    )
    
    try:
        # Get request body and headers
        try:
            body = await request.body()
            headers = dict(request.headers)
        except Exception as e:
            error_msg = f"Failed to read request body or headers: {str(e)}"
            log_auth_event(
                logger,
                "webhook_request_read_failed",
                error_msg,
                level="ERROR",
                event_data={"request_id": request_id},
                error_details={"read_error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to read request data"
            )

        # Verify webhook signature
        try:
            webhook_handler.verify_webhook_signature(body, headers)
        except WebhookSignatureError as e:
            log_auth_event(
                logger,
                "webhook_signature_rejected",
                f"Webhook signature verification failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature"
            )
        except WebhookTimestampError as e:
            log_auth_event(
                logger,
                "webhook_timestamp_rejected",
                f"Webhook timestamp validation failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook timestamp"
            )
        except ConfigurationError as e:
            log_auth_event(
                logger,
                "webhook_configuration_error",
                f"Webhook configuration error: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Webhook configuration error"
            )

        # Parse JSON payload
        try:
            event_data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON payload: {str(e)}"
            log_auth_event(
                logger,
                "webhook_payload_parse_failed",
                error_msg,
                level="ERROR",
                event_data={"request_id": request_id},
                error_details={"json_error": str(e), "body_preview": body[:200].decode('utf-8', errors='ignore')}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON payload"
            )
        except UnicodeDecodeError as e:
            error_msg = f"Invalid UTF-8 encoding in payload: {str(e)}"
            log_auth_event(
                logger,
                "webhook_payload_encoding_failed",
                error_msg,
                level="ERROR",
                event_data={"request_id": request_id},
                error_details={"encoding_error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload encoding"
            )

        # Handle the webhook event
        try:
            await webhook_handler.handle_event(event_data, db)
        except WebhookPayloadError as e:
            log_auth_event(
                logger,
                "webhook_payload_validation_failed",
                f"Webhook payload validation failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id, "event_type": event_data.get("type")},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook payload structure"
            )
        except UserCreationError as e:
            log_auth_event(
                logger,
                "webhook_user_creation_failed",
                f"User creation failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id, "event_type": event_data.get("type")},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to create user from webhook data"
            )
        except UserUpdateError as e:
            log_auth_event(
                logger,
                "webhook_user_update_failed",
                f"User update failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id, "event_type": event_data.get("type")},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to update user from webhook data"
            )
        except UserDeletionError as e:
            log_auth_event(
                logger,
                "webhook_user_deletion_failed",
                f"User deletion failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id, "event_type": event_data.get("type")},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to delete user from webhook data"
            )
        except UserNotFoundError as e:
            log_auth_event(
                logger,
                "webhook_user_not_found",
                f"User not found for webhook operation: {str(e)}",
                level="WARNING",
                event_data={"request_id": request_id, "event_type": event_data.get("type")},
                error_details=e.details
            )
            # For user not found, we return success to avoid webhook retries
            # This is common when users are deleted multiple times
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success", 
                    "event_type": event_data.get("type"),
                    "message": "User not found - operation skipped"
                }
            )
        except DatabaseOperationError as e:
            log_auth_event(
                logger,
                "webhook_database_error",
                f"Database operation failed: {str(e)}",
                level="ERROR",
                event_data={"request_id": request_id, "event_type": event_data.get("type")},
                error_details=e.details
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )

        # Success response
        event_type = event_data.get("type")
        log_auth_event(
            logger,
            "webhook_request_success",
            "Webhook event processed successfully",
            event_data={"request_id": request_id, "event_type": event_type}
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success", 
                "event_type": event_type,
                "message": "Webhook processed successfully"
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions (they're already logged above)
        raise
    except Exception as e:
        # Catch any unexpected errors
        error_msg = f"Unexpected error processing webhook: {str(e)}"
        log_auth_event(
            logger,
            "webhook_request_failed",
            error_msg,
            level="ERROR",
            event_data={"request_id": request_id},
            error_details={"unexpected_error": str(e), "error_type": type(e).__name__}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )