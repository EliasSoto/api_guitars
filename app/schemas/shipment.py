from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

# Validadores
# ge = greater than or equal
# le = less than or equal
# gt = greater than
# lt = less than

# Enumerado para el estado de seguimiento
class TrackingStatus(str, Enum):
    processing = "procesando"
    shipped = "enviado"
    in_transit = "en_transito"
    delivered = "entregado"
    cancelled = "cancelado"

# Base común para envíos
class ShipmentBase(BaseModel):
    tracking_status: TrackingStatus = Field(..., description="Estado del envío.")
    delivery_date: Optional[date] = None
    price: float = Field(..., gt=0, description="Costo del envío.")
    shipping_provider: str = Field(..., min_length=2, max_length=100, description="Proveedor del envío.")
    is_immediate_delivery: bool = Field(default=False, description="Indica si es inmediato.")
    
# Objeto para crear un envío con relación a pedidos
class ShipmentItem(BaseModel):
    order_id: int
    
    class Config:
        orm_mode = True

# Para crear un envío
class ShipmentCreate(ShipmentBase):
    order_ids: List[int] = Field(..., min_items=1, description="IDs de los pedidos asociados.")

# Para actualizar un envío
class ShipmentUpdate(BaseModel):
    shipment_date: Optional[date] = None
    tracking_status: Optional[TrackingStatus] = None
    delivery_date: Optional[date] = None
    price: Optional[float] = Field(None, gt=0)
    shipping_provider: Optional[str] = Field(None, min_length=2, max_length=100)
    is_immediate_delivery: Optional[bool] = None

# Schema para la relación ShipmentDetail
class ShipmentDetailResponse(BaseModel):
    shipment_id: int
    order_id: int
    
    class Config:
        orm_mode = True

# Para mostrar un envío
class ShipmentRead(ShipmentBase):
    shipment_date: date
    id: int
    user_id: int
    shipment_details: List[ShipmentDetailResponse] = []
    
    class Config:
        orm_mode = True

# Base para la paginación de envios
class ShipmentPagination(BaseModel):
    page: int = Field(1, ge=1, description="Número de página a obtener.")
    limit: int = Field(10, ge=1, le=100, description="Número de envíos por página.")

# Respuesta paginada para los envíos
class ShipmentListResponse(BaseModel):
    shipments: List[ShipmentRead]
    total: int

    class Config:
        orm_mode = True