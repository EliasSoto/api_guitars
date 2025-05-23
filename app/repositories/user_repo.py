from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException, status
from app.schemas import user as user_schema
from core.utils import hash_password
from app.schemas.user import UserListResponse

### FUNCIONES PARA USUARIOS ADMIN ###

# Función para crear un nuevo usuario por parte de un administrador.
def create_user_by_admin(db: Session, user: user_schema.UserCreateByAdmin):
    # Verificamos si el correo o el RUT ya están registrados.
    errors = []

    if db.query(User).filter(User.email == user.email).first():
        errors.append("El correo ya está registrado")

    if db.query(User).filter(User.rut == user.rut).first():
        errors.append("El RUT ya está registrado")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errors # Lista de errores
        )
    
    # Hasheamos la contraseña antes de guardarla.
    hashed_password = hash_password(user.hashed_password)  
    db_user = User(
        rut=user.rut,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone,
        birth_date=user.birth_date,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Función para obtener todos los usuarios.
def get_all_users(db: Session):
    return db.query(User).all()

# Función para actualizar un usuario por id.
def update_user_by_admin(db: Session, user_id: str, user: user_schema.UserAdminRead):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Se actualizan los campos del usuario.
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.rut = user.rut
    db_user.phone = user.phone
    db_user.birth_date = user.birth_date
    db_user.is_admin = user.is_admin
    

    # Se guardan los datos en la base de datos.
    db.commit()
    db.refresh(db_user)
    return db_user

# Función para eliminar un usuario por id.
def delete_user_by_admin(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Se elimina el usuario de la base de datos.
    db.delete(db_user)
    db.commit()
    return db_user


### FUNCIONES PARA USUARIOS NORMALES ###

# Función para crear un nuevo usuario por parte de un usuario normal.
def create_user(db: Session, user: user_schema.UserCreate):
    # Se verifica si el correo ya está registrado
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=["El correo ya está registrado"]
        )

    # Se verifica si el RUT ya está registrado
    if db.query(User).filter(User.rut == user.rut).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=["El RUT ya está registrado"]
        )
    
    # Hasheamos la contraseña antes de guardarla.
    hashed_password = hash_password(user.hashed_password)  
    db_user = User(
        rut=user.rut,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone,
        birth_date=user.birth_date
    )
    
    # Se agrega el nuevo usuario a la base de datos.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Función para actualizar un usuario normal logueado.
def update_normal_user(db: Session, user_id: str, user: user_schema.UserUpdate, current_user_id: str):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar los datos de otro usuario."
        )

    # Se verifica si el usuario existe.
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    # Se verifica si el correo ya está registrado por otro usuario.
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    # Se actualizan los campos del usuario.
    if user.first_name is not None:
        db_user.first_name = user.first_name
    if user.last_name is not None:
        db_user.last_name = user.last_name
    if user.email is not None:
        db_user.email = user.email
    if user.phone is not None:
        db_user.phone = user.phone

    # Se actualiza la contraseña si se proporciona una nueva.
    if user.password:
        db_user.hashed_password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user

### FUNCIONES COMPLEMENTARIAS ###

# Función que obtiene un usuario por su RUT.
def get_user_by_rut(db: Session, user_rut: str):
    return db.query(User).filter(User.rut == user_rut).first()

# Función que obtiene un usuario por su ID.
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Función que obtiene un usuario por su correo.
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#Función que obtiene un usuario por su nombre.
def get_user_by_nombres(db: Session, first_name: str):
    return db.query(User).filter(User.first_name == first_name).first()

# Función para obtener usuarios paginados.
def get_users_paginated(db: Session, page: int, limit: int):
    # Calculamos el offset basado en la página y el límite.
    offset = (page - 1) * limit

    # Consultamos los usuarios con el offset y el limit.
    users = db.query(User).offset(offset).limit(limit).all()

    # Consultamos el total de usuarios.
    total_users = db.query(User).count()

    # Si no se encuentran usuarios, lanzamos una excepción.
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron usuarios en esta página."
        )

    # Devolvemos los usuarios junto con el total.
    return UserListResponse(users=users, total=total_users)