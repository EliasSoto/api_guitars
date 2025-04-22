from pydantic import BaseModel
from typing import Optional

# Base común para reutilizar
class DireccionBase(BaseModel):
    numero_calle: str
    region: str
    comuna: str
    indicaciones: Optional[str] = None
    tipo_domicilio: str
    es_activa: Optional[bool] = True

# Para crear dirección
class DireccionCreate(DireccionBase):
    pass

# Para leer dirección desde la DB (incluye ID)
class DireccionRead(DireccionBase):
    id: int
    id_usuario: int

    class Config:
        orm_mode = True
