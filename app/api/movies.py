from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.models import db_helper
from app.core.schemas.movie import MovieRead
from app.core.services.movie_service import MovieService

router = APIRouter(
    prefix=settings.api.movies,
    tags=["Movies"],
)
 

@router.get(
    "",
    response_model=list[MovieRead],
)
async def get_movies(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    limit: int = 20,
    offset: int = 0,
):
    return await MovieService.get_movies(
        session=session,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{movie_id}",
    response_model=MovieRead,
)
async def get_movie(
    movie_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    movie = await MovieService.get_movie(
        session=session,
        movie_id=movie_id,
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found",
        )

    return movie
