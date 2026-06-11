from typing import Annotated

from fastapi import APIRouter, Depends
from app.core.config import settings
from app.core.models import db_helper
from app.core.models.users import User
from app.core.services.recommendation_service import RecommendationService
from app.core.schemas.recommendation import MovieWithScore
from app.api.dependencies.fastapi_users_conf import current_user
from ml.content_based.inference.recommend import CBRecommender
from ml.collaborative.inference.recommend import CollabRecommender
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix=settings.api.recommendations,
    tags=["Recommendations"],
)

service = RecommendationService(
    cb=CBRecommender(),
    cf=CollabRecommender(),
)


@router.get("/", response_model=list[MovieWithScore])
async def get_recommendations_for_user(
    user: Annotated[User, Depends(current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    top_n: int = 10,
):
    return await service.for_user(
        session=session,
        user_id=user.id,
        top_n=top_n,
    )


@router.get("/{movie_id}", response_model=list[MovieWithScore])
async def get_recommendations_for_movie(
    movie_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    top_n: int = 10,
):
    return await service.for_movie(
        session=session,
        movie_id=movie_id,
        top_n=top_n,
    )
