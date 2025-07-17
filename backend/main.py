from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.api.auth.webhook import router as webhooks_router
from app.config.settings import settings
from app.config.logging import setup_logging, get_auth_logger

# Configure structured logging
setup_logging()
logger = get_auth_logger("main")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(webhooks_router, prefix=f"{settings.API_V1_STR}/webhooks")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Board AI API"}
