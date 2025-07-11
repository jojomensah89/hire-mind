from fastapi import APIRouter

from app.api.v1.endpoints import users, job_listing, job_listing_application, organization, organization_user_settings, \
    user_notification_settings, user_resume

api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(job_listing.router, tags=["job_listings"])
api_router.include_router(job_listing_application.router,
                          tags=["job_listing_applications"])
api_router.include_router(organization.router, tags=["organizations"])
api_router.include_router(organization_user_settings.router,
                          tags=["organization_user_settings"])
api_router.include_router(user_notification_settings.router,
                          tags=["user_notification_settings"])
api_router.include_router(user_resume.router, tags=["user_resumes"])
