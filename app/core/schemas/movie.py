from pydantic import BaseModel


class MovieRead(BaseModel):
    id: int
    title: str
    genres: str
    year: int | None

    model_config = {
        "from_attributes": True
    }