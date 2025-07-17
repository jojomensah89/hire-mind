import hmac
import hashlib
import json
from typing import Dict, Any, Callable, Awaitable
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

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

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature from Clerk. Always enforce in production."""
        import os
        env = os.getenv("ENV", "development")
        if not self.webhook_secret:
            logger.warning("Webhook signature verification skipped - no secret configured")
            return env == "development"

        try:
            if not signature.startswith("v1,"):
                return False

            signature = signature[3:]

            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(signature, expected_signature)

        except Exception as e:
            logger.error(f"Webhook signature verification failed: {str(e)}")
            return False

    async def handle_event(self, event_data: Dict[str, Any], db: Session):
        """Handle a webhook event by dispatching it to the appropriate handler. Logs all events."""
        event_type = event_data.get("type")
        logger.info(f"Received webhook event: {event_type}", extra={"event_data": event_data})
        handler = self.event_handlers.get(event_type)
        if handler:
            try:
                await handler(event_data, db)
                logger.info(f"Successfully handled event: {event_type}")
            except Exception as e:
                logger.error(f"Error handling event {event_type}: {str(e)}", exc_info=True)
                raise
        else:
            logger.warning(f"Unhandled webhook event type: {event_type}", extra={"event_data": event_data})

    async def handle_user_created(self, event_data: Dict[str, Any], db: Session):
        """Handle user.created event"""
        try:
            clerk_user = event_data.get('data', {})
            user_service = UserService(db)
            user = user_service.create_user_from_webhook(clerk_user)
            logger.info(f"Created user: {user.id} (Clerk ID: {user.clerk_id})")
        except Exception as e:
            logger.error(f"Failed to handle user.created event: {str(e)}")
            raise

    async def handle_user_updated(self, event_data: Dict[str, Any], db: Session):
        """Handle user.updated event"""
        try:
            clerk_user = event_data.get('data', {})
            user_service = UserService(db)
            updated_user = user_service.update_user_from_webhook(clerk_user)
            if updated_user:
                logger.info(f"Updated user: {updated_user.id} (Clerk ID: {updated_user.clerk_id})")
            else:
                logger.warning(f"User not found for Clerk ID: {clerk_user.get('id')}")
        except Exception as e:
            logger.error(f"Failed to handle user.updated event: {str(e)}")
            raise

    async def handle_user_deleted(self, event_data: Dict[str, Any], db: Session):
        """Handle user.deleted event"""
        try:
            clerk_user = event_data.get('data', {})
            user_service = UserService(db)
            user_service.delete_user_from_webhook(clerk_user)
            logger.info(f"Deleted user with Clerk ID: {clerk_user.get('id')}")
        except Exception as e:
            logger.error(f"Failed to handle user.deleted event: {str(e)}")
            raise


webhook_handler = ClerkWebhookHandler(settings.CLERK_WEBHOOK_SECRET)


@router.post("/clerk")
async def clerk_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Clerk webhook events"""
    try:
        body = await request.body()
        signature = request.headers.get('svix-signature', '')

        if not webhook_handler.verify_webhook_signature(body, signature):
            logger.warning("Invalid webhook signature", extra={"headers": dict(request.headers)})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature"
            )

        try:
            event_data = json.loads(body.decode())
        except json.JSONDecodeError:
            logger.error("Invalid JSON payload", extra={"body": body})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON payload"
            )

        await webhook_handler.handle_event(event_data, db)

        logger.info("Webhook event processed successfully", extra={"event_type": event_data.get("type")})
        return JSONResponse(
            status_code=200,
            content={"status": "success", "event_type": event_data.get("type")}
        )

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}", extra={"status_code": e.status_code})
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )