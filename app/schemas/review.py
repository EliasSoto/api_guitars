from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int = Field(..., description="Valoración del 1 al 5")
    comment: Optional[str] = Field(None, description="Comentario opcional del usuario")

    @validator("rating")
    def validate_rating(cls, value):
        if not (1 <= value <= 5):
            raise ValueError("El rating debe estar entre 1 y 5")
        return value

class ReviewCreate(ReviewBase):
    guitar_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int]
    comment: Optional[str]

    @validator("rating")
    def validate_rating(cls, value):
        if value is not None and not (1 <= value <= 5):
            raise ValueError("El rating debe estar entre 1 y 5")
        return value

class ReviewRead(ReviewBase):
    id: int
    user_id: int
    guitar_id: int
    created_at: datetime

    class Config:
        orm_mode = True
