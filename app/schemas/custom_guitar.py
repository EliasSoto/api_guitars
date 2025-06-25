from pydantic import BaseModel, Field
from typing import Optional, List
from .component import ComponentRead

class ComponentDetailBase(BaseModel):
    component_id: int
    quantity: int = Field(..., gt=0)

class ComponentDetailCreate(ComponentDetailBase):
    pass

class ComponentDetailUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)

class ComponentDetailRead(ComponentDetailBase):
    component: ComponentRead

    class Config:
        orm_mode = True

class CustomGuitarBase(BaseModel):
    guitar_id: int
    custom_color: Optional[str] = Field(None, regex=r"^#(?:[0-9a-fA-F]{6})?$")
    custom_fret: Optional[int] = Field(None, ge=0)
    jack_position: Optional[str] = None

class CustomGuitarCreate(CustomGuitarBase):
    component_details: List[ComponentDetailBase] = Field(
        ..., 
        description="Lista de componentes de la guitarra."
    )

class CustomGuitarUpdate(BaseModel):
    guitar_id: Optional[int] = None
    total_price: Optional[float] = Field(None, ge=0)
    custom_color: Optional[str] = Field(None, regex=r"^#(?:[0-9a-fA-F]{6})?$")
    custom_fret: Optional[int] = Field(None, ge=0)
    jack_position: Optional[str] = None
    component_details: Optional[List[ComponentDetailBase]] = None

class CustomGuitarRead(CustomGuitarBase):
    id: int
    total_price: float
    component_details: List[ComponentDetailRead]

    class Config:
        orm_mode = True
        
class CustomGuitarListResponse(BaseModel):
    guitars: List[CustomGuitarRead]
    total: int
