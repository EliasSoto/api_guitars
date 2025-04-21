from pydantic import BaseModel, EmailStr
from typing import Optional

# Base común para todos los usuarios
class UsuarioBase(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: str
    fecha_nacimiento: str


# Registro normal de usuario (sin permisos de admin)
class UsuarioCreate(UsuarioBase):
    rut: str
    hashed_password: str

# Actualización de datos por el usuario (sin cambiar su rol ni ID)
class UsuarioUpdate(UsuarioBase):
    telefono: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    password: Optional[str] = None  # Contraseña opcional para actualizar

# Respuesta al frontend (no incluye contraseña)
class UsuarioRead(UsuarioBase):
    id: int
    rut: str
    es_administrador: bool

    class Config:
        orm_mode = True


# Creación de usuario por parte del admin (con permiso para asignar rol)
class UsuarioCreateByAdmin(UsuarioBase):
    rut: str
    hashed_password: str
    es_administrador: bool = False


# Actualización por parte del admin (puede modificar todo)
class UsuarioUpdateByAdmin(UsuarioUpdate):
    es_administrador: Optional[bool] = None



