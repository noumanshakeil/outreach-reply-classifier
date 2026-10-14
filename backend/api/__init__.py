from fastapi import APIRouter
from backend.api import health, replies, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(replies.router, prefix="/api", tags=["replies"])
api_router.include_router(ui.router, tags=["ui"])
