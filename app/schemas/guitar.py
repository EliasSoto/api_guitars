from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List
from datetime import date
from utils.guitar_validators import (validate_sale_price, validate_liquidation_price, validate_purchase_date)

# Que significa cada uno de los validadores
# ge = greater than or equal
# le = less than or equal
# gt = greater than
# lt = less than

# Base común para todas las guitarras
class GuitarBase(BaseModel):
    model: str = Field(..., min_length=2, max_length=100)
    brand: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=10, max_length=500)
    purchase_price: float = Field(..., gt=0)
    sale_price: float = Field(..., gt=0)
    purchase_date: date
    wood_type: str = Field(..., min_length=2, max_length=50)
    image_link: Optional[str] = None
    color: str = Field(..., min_length=2, max_length=30)
    stock: int = Field(..., ge=0)
    is_custom: bool = False
    fret_count: int = Field(..., ge=21, le=24)

# Para crear una guitarra
class GuitarCreate(GuitarBase):
    _validate_sale_price = validator("sale_price", allow_reuse=True)(validate_sale_price)
    _validate_purchase_date = validator("purchase_date", allow_reuse=True)(validate_purchase_date)

# Para actualizar una guitarra
class GuitarUpdate(BaseModel):
    model: Optional[str] = Field(None, min_length=2, max_length=100)
    brand: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    purchase_price: Optional[float] = Field(None, gt=0)
    sale_price: Optional[float] = Field(None, gt=0)
    liquidation_price: Optional[float] = Field(None, gt=0)
    purchase_date: Optional[date] = None
    wood_type: Optional[str] = Field(None, min_length=2, max_length=50)
    image_link: Optional[str] = None
    color: Optional[str] = Field(None, min_length=2, max_length=30)
    stock: Optional[int] = Field(None, ge=0)
    is_custom: Optional[bool] = None
    fret_count: int = Field(..., ge=21, le=24)
    
    _validate_sale_price = validator("sale_price", allow_reuse=True)(validate_sale_price)
    _validate_liquidation = validator("liquidation_price", allow_reuse=True)(validate_liquidation_price)
    _validate_purchase_date = validator("purchase_date", allow_reuse=True)(validate_purchase_date)

# Para mostrar una guitarra
class GuitarRead(GuitarBase):
    id: int
    liquidation_price: Optional[float] = None

    class Config:
        orm_mode = True
        
# Base para la paginación de guitarras
class GuitarPagination(BaseModel):
    page: int = Field(1, ge=1, description="Número de página a obtener.")
    limit: int = Field(10, ge=1, le=100, description="Número de guitarras por página.")

# Respuesta paginada para las guitarras
class GuitarListResponse(BaseModel):
    guitars: List[GuitarRead]
    total: int

    class Config:
        orm_mode = True
        
# Para mostrar solo modelo e imagen de la guitarra
class GuitarSimpleRead(BaseModel):
    model: str
    image_link: Optional[str] = None

    class Config:
        orm_mode = True
        
# Para mostrar datos al usuario
class GuitarUserRead(BaseModel):
    id: int
    model: str
    brand: str
    description: str
    sale_price: float
    wood_type: str
    image_link: Optional[str] = None
    color: str
    fret_count: int

    class Config:
        orm_mode = True