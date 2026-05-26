from fastapi import APIRouter

from app.api import admin_crawler, auth, credits, health, positions, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(credits.router, prefix="/credits", tags=["credits"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(admin_crawler.router, prefix="/admin/crawler", tags=["admin-crawler"])
