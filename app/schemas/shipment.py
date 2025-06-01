from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class TrackingStatus(str, Enum):
    processing = "procesando"
    shipped = "enviado"
    in_transit = "en_transito"
    delivered = "entregado"
    cancelled = "cancelado"

class ShipmentBase(BaseModel):
    shipment_date: Optional[date] = None
    tracking_status: TrackingStatus = Field(default=TrackingStatus.processing, description="Estado del envío.")
    delivery_date: Optional[date] = None
    price: Optional[float] = Field(default=0, ge=0, description="Costo del envío.")
    shipping_provider: Optional[str] = Field(default="por definir", min_length=2, max_length=100, description="Proveedor del envío.")
    is_immediate_delivery: Optional[bool] = Field(default=False, description="Indica si es inmediato.")

class ShipmentCreate(BaseModel):
    order_ids: List[int] = Field(..., min_items=1, description="IDs de los pedidos asociados.")

class ShipmentUpdate(BaseModel):
    shipment_date: Optional[date] = None
    tracking_status: Optional[TrackingStatus] = None
    delivery_date: Optional[date] = None
    price: Optional[float] = Field(None, ge=0)
    shipping_provider: Optional[str] = Field(None, min_length=2, max_length=100)
    is_immediate_delivery: Optional[bool] = None

class ShipmentDetailResponse(BaseModel):
    shipment_id: int
    order_id: int

    class Config:
        orm_mode = True

class ShipmentRead(ShipmentBase):
    shipment_date: Optional[date]
    id: int
    user_id: int
    shipment_details: List[ShipmentDetailResponse] = []

    class Config:
        orm_mode = True

class ShipmentPagination(BaseModel):
    page: int = Field(1, ge=1, description="Número de página a obtener.")
    limit: int = Field(10, ge=1, le=100, description="Número de envíos por página.")

class ShipmentListResponse(BaseModel):
    shipments: List[ShipmentRead]
    total: int

    class Config:
        orm_mode = True

class ShipmentStatusOnly(BaseModel):
    tracking_status: TrackingStatus
    
    class Config:
        orm_mode = True