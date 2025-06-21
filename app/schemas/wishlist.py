from pydantic import BaseModel
from typing import Optional, List

class WishlistBase(BaseModel):
    user_id: int
    guitar_id: int

class WishlistCreate(WishlistBase):
    pass

class WishlistRead(WishlistBase):
    id: int

    class Config:
        orm_mode = True

class WishlistListResponse(BaseModel):
    wishlist: List[WishlistRead]
    total: int

    class Config:
        orm_mode = True
