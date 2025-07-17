from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException, status
from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions
from clerk_backend_api.models import User as ClerkUser
from app.config.settings import settings


class ClerkAuthService:
    def __init__(self):
        self.clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
        self.authorized_parties = settings.CLERK_AUTHORIZED_PARTIES

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify a Clerk session token and return the payload
        """
        try:
            # Create a mock request with the token
            headers = {"Authorization": f"Bearer {token}"}
            request = httpx.Request("GET", "http://localhost", headers=headers)

            request_state = self.clerk.authenticate_request(
                request,
                AuthenticateRequestOptions(
                    authorized_parties=self.authorized_parties
                )
            )

            if not request_state.is_signed_in:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Authentication failed: {request_state.reason}"
                )

            return request_state.payload

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {str(e)}"
            )

    def get_user_by_id(self, user_id: str) -> Optional[ClerkUser]:
        """
        Get user details from Clerk by user ID
        """
        try:
            response = self.clerk.users.get(user_id)
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found: {str(e)}"
            )

    def get_current_user(self, token: str) -> ClerkUser:
        """
        Get current user from token
        """
        payload = self.verify_token(token)
        user_id = payload.get('sub')

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: no user ID found"
            )

        return self.get_user_by_id(user_id)

    def verify_organization_membership(self, token: str, org_id: str) -> bool:
        """
        Verify if the user is a member of the specified organization
        """
        payload = self.verify_token(token)
        user_id = payload.get('sub')

        if not user_id:
            return False

        try:
            # Get user's organization memberships
            response = self.clerk.users.get_organization_memberships(user_id)

            # Check if user is member of the specified organization
            for membership in response:
                if membership.organization.id == org_id:
                    return True

            return False

        except Exception:
            return False

    def get_user_organizations(self, token: str) -> list:
        """
        Get all organizations the user is a member of
        """
        payload = self.verify_token(token)
        user_id = payload.get('sub')

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        try:
            response = self.clerk.users.get_organization_memberships(user_id)
            return [membership.organization for membership in response]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get user organizations: {str(e)}"
            )