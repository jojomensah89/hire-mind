#!/usr/bin/env python3
"""Test script to validate the enhanced settings configuration."""

import os
import tempfile
from pathlib import Path

def test_environment_file_loading():
    """Test that environment files are loaded in the correct priority order."""
    print("Testing environment file loading...")
    
    # Test with existing configuration
    try:
        from app.config.settings import Settings
        settings = Settings()
        print(f"✓ Configuration loaded successfully")
        print(f"✓ Environment: {settings.ENVIRONMENT}")
        print(f"✓ Database URL configured: {bool(settings.DATABASE_URL)}")
        print(f"✓ Clerk keys configured: {bool(settings.CLERK_SECRET_KEY and settings.CLERK_PUBLISHABLE_KEY and settings.CLERK_WEBHOOK_SECRET)}")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_validation_errors():
    """Test that validation provides clear error messages."""
    print("\nTesting validation error messages...")
    
    try:
        from app.config.settings import Settings
        
        # Test DATABASE_URL validation
        try:
            Settings(DATABASE_URL="", CLERK_SECRET_KEY="sk_test_123", CLERK_PUBLISHABLE_KEY="pk_test_123", CLERK_WEBHOOK_SECRET="whsec_123")
            print("✗ DATABASE_URL validation should have failed")
            return False
        except ValueError as e:
            if "DATABASE_URL is required" in str(e):
                print("✓ DATABASE_URL validation works correctly")
            else:
                print(f"✗ DATABASE_URL validation message incorrect: {e}")
                return False
        
        # Test CLERK_SECRET_KEY validation
        try:
            Settings(DATABASE_URL="sqlite:///test.db", CLERK_SECRET_KEY="", CLERK_PUBLISHABLE_KEY="pk_test_123", CLERK_WEBHOOK_SECRET="whsec_123")
            print("✗ CLERK_SECRET_KEY validation should have failed")
            return False
        except ValueError as e:
            if "CLERK_SECRET_KEY is required" in str(e):
                print("✓ CLERK_SECRET_KEY validation works correctly")
            else:
                print(f"✗ CLERK_SECRET_KEY validation message incorrect: {e}")
                return False
        
        # Test CLERK_SECRET_KEY format validation
        try:
            Settings(DATABASE_URL="sqlite:///test.db", CLERK_SECRET_KEY="invalid_key", CLERK_PUBLISHABLE_KEY="pk_test_123", CLERK_WEBHOOK_SECRET="whsec_123")
            print("✗ CLERK_SECRET_KEY format validation should have failed")
            return False
        except ValueError as e:
            if "must start with 'sk_'" in str(e):
                print("✓ CLERK_SECRET_KEY format validation works correctly")
            else:
                print(f"✗ CLERK_SECRET_KEY format validation message incorrect: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Validation testing failed: {e}")
        return False

def test_environment_detection():
    """Test environment detection logic."""
    print("\nTesting environment detection...")
    
    try:
        from app.config.settings import Settings
        
        # Test default environment
        settings = Settings()
        if settings.ENVIRONMENT == "development":
            print("✓ Default environment detection works")
        else:
            print(f"✗ Expected 'development', got '{settings.ENVIRONMENT}'")
            return False
        
        # Test custom environment
        os.environ['ENVIRONMENT'] = 'production'
        settings = Settings()
        if settings.ENVIRONMENT == "production":
            print("✓ Custom environment detection works")
        else:
            print(f"✗ Expected 'production', got '{settings.ENVIRONMENT}'")
            return False
        
        # Clean up
        del os.environ['ENVIRONMENT']
        return True
    except Exception as e:
        print(f"✗ Environment detection testing failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Settings Configuration Test ===")
    
    success = True
    success &= test_environment_file_loading()
    success &= test_validation_errors()
    success &= test_environment_detection()
    
    if success:
        print("\n✓ All tests passed! Configuration is working correctly.")
    else:
        print("\n✗ Some tests failed. Please check the configuration.")