from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_backend_api.models import User as ClerkUser
from app.services.auth.clerk_auth_service import ClerkAuthService

# Initialize security scheme
security = HTTPBearer()

# Initialize Clerk service
clerk_service = ClerkAuthService()


def get_clerk_service() -> ClerkAuthService:
    """Dependency to get Clerk service instance"""
    return clerk_service


def get_token_from_header(
    authorization: Annotated[Optional[str], Header()] = None,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """Extract token from Authorization header"""
    if credentials:
        return credentials.credentials

    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid authorization header"
    )


def require_clerk_auth(
    request: Request,
    token: str = Depends(get_token_from_header),
    clerk_auth_service: ClerkAuthService = Depends(get_clerk_service),
):
    """Dependency to protect routes with Clerk authentication"""
    try:
        payload = clerk_auth_service.verify_token(token)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
        )

    request.state.user_id = payload.get('sub')
    request.state.clerk_payload = payload
    request.state.is_authenticated = True


def get_current_user(
    token: str = Depends(get_token_from_header),
    clerk_auth_service: ClerkAuthService = Depends(get_clerk_service)
) -> ClerkUser:
    """Get current authenticated user"""
    return clerk_auth_service.get_current_user(token)


def get_current_user_id(
    token: str = Depends(get_token_from_header),
    clerk_auth_service: ClerkAuthService = Depends(get_clerk_service)
) -> str:
    """Get current user ID from token"""
    payload = clerk_auth_service.verify_token(token)
    user_id = payload.get('sub')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no user ID found"
        )

    return user_id


def require_organization_membership(org_id: str):
    """Dependency factory for organization membership verification"""

    def verify_membership(
        token: str = Depends(get_token_from_header),
        clerk_auth_service: ClerkAuthService = Depends(get_clerk_service)
    ) -> bool:
        if not clerk_auth_service.verify_organization_membership(token, org_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of the required organization"
            )
        return True

    return verify_membership


def get_user_organizations(
    token: str = Depends(get_token_from_header),
    clerk_auth_service: ClerkAuthService = Depends(get_clerk_service)
) -> list:
    """Get user's organizations"""
    return clerk_auth_service.get_user_organizations(token)