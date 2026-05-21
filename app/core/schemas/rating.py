from pydantic import BaseModel


class RatingCreate(BaseModel):
    movie_id: int
    rating: int


class RatingRead(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int
    created_at: int
