"""
Custom exceptions for authentication operations
"""
from typing import Optional, Dict, Any


class AuthenticationError(Exception):
    """Base exception for authentication-related errors"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class WebhookSignatureError(AuthenticationError):
    """Raised when webhook signature verification fails"""
    pass


class WebhookTimestampError(AuthenticationError):
    """Raised when webhook timestamp is invalid or outside acceptable range"""
    pass


class WebhookPayloadError(AuthenticationError):
    """Raised when webhook payload is malformed or invalid"""
    pass


class UserNotFoundError(AuthenticationError):
    """Raised when a user cannot be found by ID or Clerk ID"""
    pass


class UserCreationError(AuthenticationError):
    """Raised when user creation fails"""
    pass


class UserUpdateError(AuthenticationError):
    """Raised when user update fails"""
    pass


class UserDeletionError(AuthenticationError):
    """Raised when user deletion fails"""
    pass


class DatabaseOperationError(AuthenticationError):
    """Raised when database operations fail during authentication operations"""
    pass


class ConfigurationError(AuthenticationError):
    """Raised when authentication configuration is invalid or missing"""
    pass