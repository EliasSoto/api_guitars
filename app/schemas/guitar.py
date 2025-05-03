from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# Que significa cada uno de los validadores
# ge = greater than or equal
# le = less than or equal
# gt = greater than
# lt = less than

# Base común para todas las guitarras
class GuitarBase(BaseModel):
    model: str = Field(..., min_length=2, max_length=100)
    purchase_price: float = Field(..., gt=0)
    sale_price: float = Field(..., gt=0)
    net_price: float = Field(..., gt=0)
    iva: float = Field(..., ge=0, le=1)
    liquidation_price: float = Field(..., gt=0)
    purchase_date: date
    wood_type: str = Field(..., min_length=2, max_length=50)
    image_link: Optional[str] = None
    color: str = Field(..., min_length=2, max_length=30)
    stock: int = Field(..., ge=0)
    is_custom: bool = False
    fret_count: int = Field(..., ge=21, le=24)

# Para crear una guitarra
class GuitarCreate(GuitarBase):
    pass 

# Para actualizar una guitarra
class GuitarUpdate(BaseModel):
    model: Optional[str] = Field(None, min_length=2, max_length=100)
    purchase_price: Optional[float] = Field(None, gt=0)
    sale_price: Optional[float] = Field(None, gt=0)
    net_price: Optional[float] = Field(None, gt=0)
    iva: Optional[float] = Field(None, ge=0, le=1)
    liquidation_price: Optional[float] = Field(None, gt=0)
    purchase_date: Optional[date] = None
    wood_type: Optional[str] = Field(None, min_length=2, max_length=50)
    image_link: Optional[str] = None
    color: Optional[str] = Field(None, min_length=2, max_length=30)
    stock: Optional[int] = Field(None, ge=0)
    is_custom: Optional[bool] = None
    fret_count: Optional[int] = Field(None, ge=1)

# Para mostrar una guitarra
class GuitarRead(GuitarBase):
    id: int

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