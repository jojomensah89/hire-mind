#!/usr/bin/env python3
"""
Simple test to verify error handling and logging functionality
"""
import sys
import os
sys.path.append('.')

from app.exceptions.auth_exceptions import (
    AuthenticationError,
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
from app.config.logging import setup_logging, get_auth_logger, log_auth_event

def test_exceptions():
    """Test that all custom exceptions work correctly"""
    print("Testing custom exceptions...")
    
    # Test base exception
    try:
        raise AuthenticationError("Test error", {"detail": "test"})
    except AuthenticationError as e:
        assert e.message == "Test error"
        assert e.details == {"detail": "test"}
        print("✓ AuthenticationError works")
    
    # Test specific exceptions
    exceptions_to_test = [
        WebhookSignatureError,
        WebhookTimestampError,
        WebhookPayloadError,
        UserNotFoundError,
        UserCreationError,
        UserUpdateError,
        UserDeletionError,
        DatabaseOperationError,
        ConfigurationError
    ]
    
    for exc_class in exceptions_to_test:
        try:
            raise exc_class("Test message", {"test": "data"})
        except AuthenticationError as e:
            assert e.message == "Test message"
            assert e.details == {"test": "data"}
            print(f"✓ {exc_class.__name__} works")

def test_logging():
    """Test that structured logging works correctly"""
    print("\nTesting structured logging...")
    
    # Setup logging
    setup_logging("DEBUG")
    logger = get_auth_logger("test")
    
    # Test basic logging
    logger.info("Test log message")
    print("✓ Basic logging works")
    
    # Test structured auth logging
    log_auth_event(
        logger,
        "test_event",
        "Test authentication event",
        level="INFO",
        user_id="test-user-123",
        clerk_id="clerk-456",
        event_data={"test": "data"},
        error_details={"error": "none"}
    )
    print("✓ Structured auth logging works")

def main():
    """Run all tests"""
    print("Running error handling and logging tests...\n")
    
    try:
        test_exceptions()
        test_logging()
        print("\n✅ All tests passed!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())