from fastapi import APIRouter

from app.core.config import settings
from .auth import router as auth_router
router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(
    router=auth_router,
)