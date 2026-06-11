from fastapi import APIRouter

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.movies import router as movies_router
from app.api.ratings import router as ratings_router
from app.api.recommendations import router as recommendations_router

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(
    router=auth_router,
)
router.include_router(
    router=movies_router,
)
router.include_router(
    router=ratings_router,
)
router.include_router(
    router=recommendations_router,
)