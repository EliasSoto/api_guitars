from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from utils.component_validators import (validate_sale_price, validate_purchase_date, validate_is_active, validate_subtype)

class ComponentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    type: str = Field(..., min_length=2, max_length=50)
    subtype: Optional[str] = Field(None, max_length=50)
    purchase_price: float = Field(..., gt=0)
    sale_price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    purchase_date: date
    brand: Optional[str] = Field(None, min_length=2, max_length=50)
    material: Optional[str] = Field(None, min_length=2, max_length=50)
    image_link: Optional[str] = None
    is_active: Optional[bool] = True

class ComponentCreate(ComponentBase):
    _validate_sale_price = validator("sale_price", allow_reuse=True)(validate_sale_price)
    _validate_purchase_date = validator("purchase_date", allow_reuse=True)(validate_purchase_date)
    _validate_is_active = validator("is_active", allow_reuse=True)(validate_is_active)
    _validate_subtype = validator("subtype", allow_reuse=True)(validate_subtype)
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
    image_link: Optional[str]
    is_active: Optional[bool]
    
    _validate_sale_price = validator("sale_price", allow_reuse=True)(validate_sale_price)
    _validate_purchase_date = validator("purchase_date", allow_reuse=True)(validate_purchase_date)
    _validate_is_active = validator("is_active", allow_reuse=True)(validate_is_active)
    _validate_subtype = validator("subtype", allow_reuse=True)(validate_subtype)

class ComponentRead(ComponentBase):
    id: int
    net_price: float

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