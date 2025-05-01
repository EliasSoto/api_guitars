from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from core.utils import validate_rut, validate_phone_number
from datetime import date

# Base común para todos los usuarios. (Se usa para crear y leer usuarios, para actualizar se usa un BaseModel)
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=9, max_length=9)
    birth_date: date = Field(..., description="Fecha de nacimiento en formato YYYY-MM-DD")

# Registro normal de usuario. (sin permisos de admin)
class UserCreate(UserBase):
    rut: str = Field(..., min_length=8, max_length=12)
    hashed_password: str = Field(..., min_length=8, max_length=20)  # Contraseña obligatoria.
    
    # Validaciones personalizadas para los campos.
    _validate_rut = validator('rut', allow_reuse=True)(validate_rut)
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)

# Actualización de datos por el usuario. (sin cambiar su rol ni ID)
class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=9, max_length=9)
    birth_date: Optional[date] = None
    password: Optional[str] = Field(None, min_length=8, max_length=20)
    
    ## Validaciones personalizadas para los campos.
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)

# Respuesta al frontend. (no incluye contraseña)
class UserRead(UserBase):
    id: int
    rut: str
    is_admin: bool

    class Config:
        orm_mode = True

# Creación de usuario por parte del admin (con permiso para asignar rol)
class UserCreateByAdmin(UserBase):
    rut: str = Field(..., min_length=8, max_length=12)
    hashed_password: str = Field(..., min_length=8, max_length=20)  # Contraseña obligatoria.
    is_admin: bool = False
    
    # Validaciones personalizadas para los campos.
    _validate_rut = validator('rut', allow_reuse=True)(validate_rut)
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)

# Actualización por parte del admin (sin contraseña)
class UserUpdateByAdmin(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=9, max_length=9)
    birth_date: Optional[date] = None
    rut: Optional[str] = Field(..., min_length=8, max_length=12)
    is_admin: Optional[bool] = None
    
    # Validaciones personalizadas para los campos.
    _validate_rut = validator('rut', allow_reuse=True)(validate_rut)
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)

    class Config:
        orm_mode = True

# Respuesta al frontend para el admin (sin contraseña)
class UserAdminRead(UserBase):
    rut: str
    is_admin: bool
    
    class Config:
        orm_mode = True
