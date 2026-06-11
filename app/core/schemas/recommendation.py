from app.core.schemas.movie import MovieRead

class MovieWithScore(MovieRead):
    score: float