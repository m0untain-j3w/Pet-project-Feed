from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.users import User
from core.models import db_helper
from core.schemas.rating import RatingCreate, RatingRead
from core.config import settings
from api.dependencies.fastapi_users_conf import current_user
from core.services.rating_service import RatingService

router = APIRouter(
    prefix=settings.api.ratings,
    tags=["Ratings"],
)


@router.post("/", response_model=RatingRead)
async def set_rating(
    user: Annotated[User, Depends(current_user)],
    rating_data: RatingCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await RatingService.rate_movie(
        session=session,
        user_id=user.id,
        rating_data=rating_data,
    )


@router.get("/my", response_model=list[RatingRead])
async def get_my_ratings(
    user: Annotated[User, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await RatingService.get_user_ratings(
        session=session,
        user_id=user.id,
    )
