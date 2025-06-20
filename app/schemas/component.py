from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class CompatibilityEnum(str, Enum):
    strato = "Strato"
    telecaster = "Telecaster"
    sg = "SG"
    les_paul = "Les Paul"
    flying_v = "Flying V"

class ComponentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    type: str = Field(..., min_length=2, max_length=50)
    subtype: Optional[str] = Field(None, max_length=50)
    purchase_price: float = Field(..., gt=0)
    sale_price: float = Field(..., gt=0)
    net_price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    purchase_date: date
    brand: Optional[str] = Field(None, min_length=2, max_length=50)
    material: Optional[str] = Field(None, min_length=2, max_length=50)
    position: Optional[str] = Field(None, min_length=2, max_length=50)
    compatibility: Optional[List[CompatibilityEnum]] = []
    is_active: Optional[bool] = True

class ComponentCreate(ComponentBase):
    pass

class ComponentUpdate(BaseModel):
    name: Optional[str]
    type: Optional[str]
    subtype: Optional[str]
    purchase_price: Optional[float]
    sale_price: Optional[float]
    net_price: Optional[float]
    stock: Optional[int]
    description: Optional[str]
    purchase_date: Optional[date]
    brand: Optional[str]
    material: Optional[str]
    position: Optional[str]
    compatibility: Optional[List[CompatibilityEnum]] = None
    is_active: Optional[bool]

class ComponentRead(ComponentBase):
    id: int

    class Config:
        orm_mode = True

class ComponentPagination(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)

class ComponentListResponse(BaseModel):
    components: List[ComponentRead]
    total: int

    class Config:
        orm_mode = True