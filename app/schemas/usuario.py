from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema Base - Propiedades comunes para el usuario
class UsuarioBase(BaseModel):
    rut: str
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: str = None
    fecha_nacimiento: str = None
    es_administrador: bool = False
    
### Schemas para usuario ###
# Schema para crear un nuevo usuario
class UsuarioCreate(UsuarioBase):
    password: str  # Hashear más adelante

# Schema para leer un usuario existente
class UsuarioRead(UsuarioBase):
    id: int
    rut: str
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: str = None
    fecha_nacimiento: str = None

    class Config:
        orm_mode = True
        
# Schema para actualizar un usuario existente
class UsuarioUpdate(BaseModel):
    nombres: Optional[str]
    apellidos: Optional[str]
    telefono: Optional[str]
    password: Optional[str]
        
### Schemas para administrador ###
# Schema para crear un nuevo usuario por parte de un administrador
class UsuarioAdminCreate(UsuarioBase):
    password: str  # Hashear más adelante
    es_administrador: bool
    
# Schema para leer un usuario existente
class UsuarioAdminRead(UsuarioBase):
    id: int
    rut: str
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: str = None
    fecha_nacimiento: str = None
    es_administrador: bool

    class Config:
        orm_mode = True
        
# Schema para actualizar un usuario existente
class UsuarioUpdate(BaseModel):
    nombres: Optional[str]
    apellidos: Optional[str]
    telefono: Optional[str]
    password: Optional[str]