from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Título de la película", min_length=5, max_length=60)
    overview: str = Field(default="Descripción de la película", min_length=15, max_length=300)
    year: int = Field(default=2023)
    rating: float = Field(ge=1.0, le=10.0)
    category: str = Field(default="Drama", min_length=3, max_length=15)
