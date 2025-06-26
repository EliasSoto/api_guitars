from pydantic import BaseModel, Field, root_validator
from typing import Optional, List
from datetime import date
from app.schemas.guitar import GuitarRead
from app.schemas.custom_guitar import CustomGuitarRead
from enum import Enum

# Validadores
# ge = greater than or equal
# le = less than or equal
# gt = greater than
# lt = less than

# Enumerado para el estado de pedido
class OrderStatus(str, Enum):
    pending = "por pagar"
    processed = "pagado"
    cancelled = "cancelado"

# Base común para pedidos
class OrderBase(BaseModel):
    status:OrderStatus = Field(..., description="Estado del pedido.")
    payment_method: str = Field(..., min_length=2, max_length=50)
    
# Objeto para crear un una guitarra con cantidad
class OrderItem(BaseModel):
    guitar_id: Optional[int] = None
    custom_guitar_id: Optional[int] = None
    quantity: int = Field(..., gt=0)
    
    @root_validator(pre=True)
    def validate_item(cls, values):
        guitar_id = values.get("guitar_id")
        custom_guitar_id = values.get("custom_guitar_id")
        
        if guitar_id is None and custom_guitar_id is None:
            raise ValueError("Debe incluir al menos 'guitar_id' o 'custom_guitar_id'.")
        if guitar_id is not None and custom_guitar_id is not None:
            raise ValueError("Solo se debe incluir uno: 'guitar_id' o 'custom_guitar_id'.")
        return values
    
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
    guitar: Optional[GuitarRead] = None
    custom_guitar: Optional[CustomGuitarRead] = None
    quantity: int
    unit_price: float = Field(..., gt=0, description="Precio unitario aplicado a la guitarra.")
    total_price: float = Field(..., gt=0, description="Precio total por la cantidad de guitarras.")
    
    class Config:
        orm_mode = True

# Para mostrar pedido
class OrderRead(OrderBase):
    id: int
    user_id: int
    order_date: date = Field(..., description="Fecha del pedido.")
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