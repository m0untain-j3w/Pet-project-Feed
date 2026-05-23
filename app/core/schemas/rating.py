from datetime import datetime

from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    movie_id: int
    rating: int = Field(ge=1, le=5)


class RatingRead(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    created_at: datetime
