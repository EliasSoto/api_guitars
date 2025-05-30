from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from app.schemas.guitar import GuitarRead
from enum import Enum

# Validadores
# ge = greater than or equal
# le = less than or equal
# gt = greater than
# lt = less than

# Enumerado para el estado de pedido
class OrderStatus(str, Enum):
    pending = "pendiente"
    completed = "completado"
    cancelled = "cancelado"


# Base común para pedidos
class OrderBase(BaseModel):
    order_date: date
    status:OrderStatus = Field(..., description="Estado del pedido.")
    payment_method: str = Field(..., min_length=2, max_length=50)
    
# Objeto para crear un una guitarra con cantidad
class OrderItem(BaseModel):
    guitar_id: int
    quantity: int = Field(..., gt=0)
    
# Para crear pedido
class OrderCreate(OrderBase):
    items: List[OrderItem] = Field(..., description="Lista de guitarras con cantidad para el pedido.")

# Para actualizar pedido
class OrderUpdate(BaseModel):
    order_date: Optional[date] = None
    total_price: Optional[float] = Field(None, gt=0)
    status: Optional[OrderStatus] = Field(None, description="Estado del pedido.")
    payment_method: Optional[str] = Field(None, min_length=2, max_length=50)

# Schema para la relación OrderDetail
class OrderDetailResponse(BaseModel):
    guitar: GuitarRead
    quantity: int
    
    class Config:
        orm_mode = True

# Para mostrar pedido
class OrderRead(OrderBase):
    id: int
    user_id: int
    total_price: float = Field(..., gt=0, description="Precio total del pedido.")
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