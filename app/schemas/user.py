from pydantic import BaseModel, EmailStr
from typing import Optional

# Base común para todos los usuarios.
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birth_date: str


# Registro normal de usuario. (sin permisos de admin)
class UserCreate(UserBase):
    rut: str
    hashed_password: str

# Actualización de datos por el usuario. (sin cambiar su rol ni ID)
class UserUpdate(UserBase):
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None  # Contraseña opcional para actualizarla.

# Respuesta al frontend. (no incluye contraseña)
class UserRead(UserBase):
    id: int
    rut: str
    is_admin: bool

    class Config:
        orm_mode = True


# Creación de usuario por parte del admin (con permiso para asignar rol)
class UserCreateByAdmin(UserBase):
    rut: str
    hashed_password: str
    is_admin: bool = False


# Actualización por parte del admin (sin contraseña)
class UserUpdateByAdmin(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    rut: Optional[str] = None
    is_admin: Optional[bool] = None  # Rol de admin opcional

    class Config:
        orm_mode = True

# Respuesta al frontend para el admin (incluye rol y no contraseña)
class UserAdminRead(UserBase):
    rut: str
    is_admin: bool
    
    class Config:
        orm_mode = True

