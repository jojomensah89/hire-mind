import os
from typing import List, Optional
from pydantic import field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


def load_environment_file():
    """Load the appropriate environment file based on the ENVIRONMENT variable."""
    # Get environment from system environment variables first
    environment = os.getenv('ENVIRONMENT', 'development').lower()
    
    # Define environment file mapping
    env_file_mapping = {
        'development': '.env.dev',
        'dev': '.env.dev',
        'production': '.env.prod',
        'prod': '.env.prod',
        'staging': '.env.staging',
        'test': '.env.test',
        'local': '.env.local'
    }
    
    # Priority order for loading environment files
    env_files_to_try = [
        '.env.local',  # Highest priority - local overrides
        env_file_mapping.get(environment, '.env.dev'),  # Environment-specific file
        '.env'  # Default fallback
    ]
    
    loaded_files = []
    for env_file in env_files_to_try:
        if os.path.exists(env_file):
            load_dotenv(env_file, override=False)  # Don't override already set variables
            loaded_files.append(env_file)
    
    if loaded_files:
        print(f"Loaded environment files: {', '.join(loaded_files)} for environment: {environment}")
    else:
        print(f"No environment files found for environment: {environment}, using system environment variables")
    
    return environment, loaded_files


# Load environment files before class definition
current_environment, loaded_env_files = load_environment_file()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Board AI"
    API_V1_STR: str = "/api/v1"
    
    # Environment detection
    ENVIRONMENT: str = current_environment
    
    # Dynamic environment file selection based on environment
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Database settings
    DATABASE_URL: Optional[str] = None

    # JWT settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]

    # Clerk settings
    CLERK_SECRET_KEY: Optional[str] = None
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    CLERK_WEBHOOK_SECRET: Optional[str] = None
    CLERK_AUTHORIZED_PARTIES: List[str] = ["http://localhost:3000"]

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str, info: ValidationInfo) -> str:
        if not v:
            raise ValueError(
                "DATABASE_URL is required. Please set it in your environment file or as an environment variable. "
                "Example: DATABASE_URL=sqlite:///./job-board.db"
            )
        return v

    @field_validator('CLERK_SECRET_KEY')
    @classmethod
    def validate_clerk_secret_key(cls, v: str, info: ValidationInfo) -> str:
        if not v:
            raise ValueError(
                "CLERK_SECRET_KEY is required for authentication. "
                "Please set it in your environment file or as an environment variable. "
                "Get your secret key from the Clerk dashboard."
            )
        if not v.startswith('sk_'):
            raise ValueError(
                "CLERK_SECRET_KEY must start with 'sk_'. "
                "Please check your Clerk secret key format."
            )
        return v

    @field_validator('CLERK_PUBLISHABLE_KEY')
    @classmethod
    def validate_clerk_publishable_key(cls, v: str, info: ValidationInfo) -> str:
        if not v:
            raise ValueError(
                "CLERK_PUBLISHABLE_KEY is required for frontend authentication. "
                "Please set it in your environment file or as an environment variable. "
                "Get your publishable key from the Clerk dashboard."
            )
        if not v.startswith('pk_'):
            raise ValueError(
                "CLERK_PUBLISHABLE_KEY must start with 'pk_'. "
                "Please check your Clerk publishable key format."
            )
        return v

    @field_validator('CLERK_WEBHOOK_SECRET')
    @classmethod
    def validate_clerk_webhook_secret(cls, v: str, info: ValidationInfo) -> str:
        if not v:
            raise ValueError(
                "CLERK_WEBHOOK_SECRET is required for webhook signature verification. "
                "Please set it in your environment file or as an environment variable. "
                "Get your webhook secret from the Clerk dashboard webhook configuration."
            )
        if not v.startswith('whsec_'):
            raise ValueError(
                "CLERK_WEBHOOK_SECRET must start with 'whsec_'. "
                "Please check your Clerk webhook secret format."
            )
        return v

    def model_post_init(self, __context) -> None:
        """Post-initialization hook to log configuration loading."""
        # Log which environment files were loaded
        if loaded_env_files:
            print(f"Configuration loaded from environment files: {', '.join(loaded_env_files)}")
        else:
            print("No environment files found, using environment variables and defaults")
        
        print(f"Environment: {self.ENVIRONMENT}")
        print(f"Configuration validation completed successfully")

def get_settings() -> Settings:
    """Factory function to create settings instance with proper error handling."""
    try:
        return Settings()
    except Exception as e:
        print(f"Configuration Error: {str(e)}")
        print("\nConfiguration Help:")
        print("1. Ensure you have a .env file with required variables")
        print("2. Check that all Clerk keys are properly formatted")
        print("3. Verify DATABASE_URL is set correctly")
        print("4. See .env.example for reference configuration")
        raise

settings = get_settings()