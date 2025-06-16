from pydantic import BaseModel, Field
from typing import Optional, List
from .component import ComponentRead

# Component Detail Models
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

# Custom Guitar Models
class CustomGuitarBase(BaseModel):
    guitar_id: int

class CustomGuitarCreate(CustomGuitarBase):
    component_details: List[ComponentDetailBase] = Field(
        ..., 
        description="List of components for the custom guitar."
    )

class CustomGuitarUpdate(BaseModel):
    guitar_id: Optional[int] = None
    total_price: Optional[float] = Field(None, ge=0)
    component_details: Optional[List[ComponentDetailBase]] = None

class CustomGuitarRead(CustomGuitarBase):
    id: int
    component_details: List[ComponentDetailRead]

    class Config:
        orm_mode = True
        
class CustomGuitarListResponse(BaseModel):
    guitars: List[CustomGuitarRead]
    total: int
