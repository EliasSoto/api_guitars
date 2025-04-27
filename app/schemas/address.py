from pydantic import BaseModel
from typing import Optional

# Base común para reutilizar
class AddressBase(BaseModel):
    street_name: str
    region: str
    commune: str
    directions: Optional[str] = None
    address_type: str
    is_active: Optional[bool] = True

# Para crear dirección
class AddressCreate(AddressBase):
    pass

# Para leer dirección desde la DB (incluye ID)
class AddressRead(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Para actualizar dirección
class AddressUpdate(AddressBase):
    street_name: Optional[str] = None
    region: Optional[str] = None
    commune: Optional[str] = None
    directions: Optional[Optional[str]] = None
    address_type: Optional[str] = None
    is_active: Optional[bool] = None