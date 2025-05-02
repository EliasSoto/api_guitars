from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from app.schemas.guitar import GuitarRead
from enum import Enum

# Validadores (como los tenías)
# ge = greater than or equal
# le = less than or equal
# gt = greater than
# lt = less than

class OrderStatus(str, Enum):
    pending = "pendiente"
    completed = "completado"
    cancelled = "cancelado"


# Base común para pedidos
class OrderBase(BaseModel):
    order_date: date
    total_price: float = Field(..., gt=0)
    status:OrderStatus = Field(..., description="Estado del pedido.")
    payment_method: str = Field(..., min_length=2, max_length=50)
    quantity: int = Field(..., ge=1)
    guitar_ids: List[int] = Field(..., description="Lista de IDs de guitarras en el pedido.")

# Para crear pedido
class OrderCreate(OrderBase):
    pass 

# Para actualizar pedido
class OrderUpdate(BaseModel):
    order_date: Optional[date] = None
    total_price: Optional[float] = Field(None, gt=0)
    status: Optional[OrderStatus] = Field(None, description="Estado del pedido.")
    payment_method: Optional[str] = Field(None, min_length=2, max_length=50)
    quantity: Optional[int] = Field(None, ge=1)

# Schema para la relación OrderDetail
class OrderDetailResponse(BaseModel):
    guitar: GuitarRead
    
    class Config:
        orm_mode = True

# Para mostrar pedido
class OrderRead(OrderBase):
    id: int
    user_id: int
    guitar_ids: List[int] = []
    order_details: List[OrderDetailResponse] = []

    class Config:
        orm_mode = True
        
# Base para la paginación de pedidos
class OrderPagination(BaseModel):
    page: int = Field(1, ge=1, description="Número de página a obtener.")
    limit: int = Field(10, ge=1, le=100, description="Número de pedidos por página.")

# Respuesta paginada para los pedidos
class OrderListResponse(BaseModel):
    orders: List[OrderRead]
    total: int

    class Config:
        orm_mode = True