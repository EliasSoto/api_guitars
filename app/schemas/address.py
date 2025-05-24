from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

# Base común para reutilizar
class AddressBase(BaseModel):
    street_name: str = Field(..., min_length=2, max_length=100, description="Nombre de la calle y número")
    region: str = Field(..., min_length=2, max_length=50, description="Región")
    commune: str = Field(..., min_length=2, max_length=50, description="Comuna")
    directions: Optional[str] = Field(None, max_length=200, description="Indicaciones adicionales")
    address_type: str = Field(..., min_length=2, max_length=50, description="Tipo de dirección")
    is_active: bool = Field(True, description="Indica si es la dirección activa")

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
    street_name: Optional[str] = Field(None, min_length=2, max_length=100)
    region: Optional[str] = Field(None, min_length=2, max_length=50)
    commune: Optional[str] = Field(None, min_length=2, max_length=50)
    directions: Optional[str] = Field(None, max_length=200)
    address_type: Optional[str] = Field(None, min_length=2, max_length=50)
    is_active: Optional[bool] = Field(None, description="Al activar, desactiva las demás")