from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from core.utils import validate_rut, validate_phone_number, validate_birth_date

# Base común para todos los usuarios.
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str
    birth_date: str

# Registro normal de usuario. (sin permisos de admin)
class UserCreate(UserBase):
    rut: str
    hashed_password: str = Field(..., min_length=4, max_length=20)  # Contraseña obligatoria.
    
    # Validación del RUT.
    _validate_rut = validator('rut', allow_reuse=True)(validate_rut)
    
    # Validación del número de teléfono.
    @validator('phone')
    def phone_must_be_valid(cls, v):
        return validate_phone_number(v)
    
    # Validación del formato de la fecha de nacimiento y rango aceptable.
    @validator('birth_date')
    def birth_date_must_be_valid(cls, v):
        return validate_birth_date(v)

# Actualización de datos por el usuario. (sin cambiar su rol ni ID)
class UserUpdate(UserBase):
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8, max_length=20)  # Contraseña opcional.
    
    # Validación del número de teléfono.
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)
    
    # Validación del formato de la fecha de nacimiento y rango aceptable.
    _validate_birth_date = validator('birth_date', allow_reuse=True)(validate_birth_date)

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
    hashed_password: str = Field(..., min_length=8, max_length=20)  # Contraseña obligatoria.
    is_admin: bool = False
    
    # Validación del RUT.
    _validate_rut = validator('rut', allow_reuse=True)(validate_rut)
    
    # Validación del número de teléfono.
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)
    
    # Validación del formato de la fecha de nacimiento y rango aceptable.
    _validate_birth_date = validator('birth_date', allow_reuse=True)(validate_birth_date)


# Actualización por parte del admin (sin contraseña)
class UserUpdateByAdmin(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    rut: Optional[str] = None
    is_admin: Optional[bool] = None  # Rol de admin opcional
    
    # Validación del RUT.
    _validate_rut = validator('rut', allow_reuse=True)(validate_rut)
    
    # Validación del número de teléfono.
    _validate_phone = validator('phone', allow_reuse=True)(validate_phone_number)
    
    # Validación del formato de la fecha de nacimiento y rango aceptable.
    _validate_birth_date = validator('birth_date', allow_reuse=True)(validate_birth_date)

    class Config:
        orm_mode = True

# Respuesta al frontend para el admin (incluye rol y no contraseña)
class UserAdminRead(UserBase):
    rut: str
    is_admin: bool
    
    class Config:
        orm_mode = True
