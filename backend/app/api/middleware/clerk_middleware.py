from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import httpx
from app.services.auth.clerk_auth_service import ClerkAuthService
import logging

logger = logging.getLogger(__name__)


class ClerkAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle Clerk authentication for protected routes
    """

    def __init__(self, app: ASGIApp, protected_paths: list[str] = None):
        super().__init__(app)
        self.clerk_service = ClerkAuthService()
        self.protected_paths = protected_paths or []

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public paths
        if not self._is_protected_path(request.url.path):
            response = await call_next(request)
            return response

        # Extract token from request
        token = self._extract_token(request)

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing authorization token"}
            )

        try:
            # Verify token with Clerk
            payload = self.clerk_service.verify_token(token)

            # Add user info to request state
            request.state.user_id = payload.get('sub')
            request.state.clerk_payload = payload
            request.state.is_authenticated = True

            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

    def _is_protected_path(self, path: str) -> bool:
        """Check if the path requires authentication"""
        # Skip authentication for docs, health checks, etc.
        public_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/api/v1/auth/webhook",  # Clerk webhook endpoint
        ]

        if path in public_paths:
            return False

        # Check if path starts with any protected path
        for protected_path in self.protected_paths:
            if path.startswith(protected_path):
                return True

        return False

    def _extract_token(self, request: Request) -> str:
        """Extract token from Authorization header"""
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            return None

        return auth_header.replace("Bearer ", "")


# Alternative: Route-specific middleware
class ClerkRouteMiddleware:
    """
    Route-specific middleware for Clerk authentication
    """

    def __init__(self):
        self.clerk_service = ClerkAuthService()

    async def __call__(self, request: Request, call_next):
        token = self._extract_token(request)

        if not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing authorization token"}
            )

        try:
            payload = self.clerk_service.verify_token(token)
            request.state.user_id = payload.get('sub')
            request.state.clerk_payload = payload
            request.state.is_authenticated = True

            response = await call_next(request)
            return response

        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Authentication failed: {str(e)}"}
            )

    def _extract_token(self, request: Request) -> str:
        """Extract token from Authorization header"""
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        return auth_header.replace("Bearer ", "")
