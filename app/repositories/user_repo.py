from sqlalchemy.orm import Session
from models.usuario import Usuario
from fastapi import HTTPException, status
from schemas import usuario as usuario_schema
from core.utils import hash_password

#Repositorio de usuarios LISTO

#FUNCIONES PARA USUARIOS ADMIN

#FUNCIÓN CREATE
def create_user_by_admin(db: Session, user: usuario_schema.UsuarioCreateByAdmin):
    # Verificamos si el correo o el RUT ya están registrados
    errores = []

    if db.query(Usuario).filter(Usuario.correo == user.correo).first():
        errores.append("El correo ya está registrado")

    if db.query(Usuario).filter(Usuario.rut == user.rut).first():
        errores.append("El RUT ya está registrado")

    if errores:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errores # Lista de errores
        )
    
    # Hasheamos la contraseña antes de guardarla
    hashed_password = hash_password(user.hashed_password)  
    db_user = Usuario(
        rut=user.rut,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        hashed_password=hashed_password,  
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento,
        es_administrador=user.es_administrador
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#FUNCIÓN READ
def get_all_users(db: Session):
    return db.query(Usuario).all()

#FUNCIÓN UPDATE
def update_user_by_admin(db: Session, user_rut: str, user: usuario_schema.UsuarioUpdateByAdmin):
    db_user = db.query(Usuario).filter(Usuario.rut == user_rut).first()
    if not db_user:
        return None

    # Actualizar los campos del usuario
    db_user.nombres = user.nombres
    db_user.apellidos = user.apellidos
    db_user.correo = user.correo
    db_user.telefono = user.telefono
    db_user.fecha_nacimiento = user.fecha_nacimiento
    db_user.es_administrador = user.es_administrador

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(db_user)
    return db_user

#FUNCIÓN DELETE
def delete_user_by_admin(db: Session, user_rut: str):
    db_user = db.query(Usuario).filter(Usuario.rut == user_rut).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
#FUNCIONES PARA USUARIOS ADMIN


#FUNCIONES PARA USUARIOS NORMALES

#funcion para registrarse y que ademas no puedas si estas registrado en la api
def create_user(db: Session, user: usuario_schema.UsuarioCreate):
    # Verificamos si el correo o el RUT ya están registrados
    errores = []

    if db.query(Usuario).filter(Usuario.correo == user.correo).first():
        errores.append("El correo ya está registrado")

    if db.query(Usuario).filter(Usuario.rut == user.rut).first():
        errores.append("El RUT ya está registrado")

    if errores:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=errores # Lista de errores
        )
        
    hashed_password = hash_password(user.hashed_password)  # Hasheamos la contraseña antes de guardarla  
    db_user = Usuario(
        rut=user.rut,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        hashed_password=hashed_password,  # Nueva contraseña hasheada
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Actualizar usuario normal, los datos se obtienen por sesión.
def update_normal_user(db: Session, user_rut: str, user: usuario_schema.UsuarioUpdate, current_user_rut: str):
    if user_rut != current_user_rut:
        raise PermissionError("No tienes permiso para modificar los datos de otro usuario.")

    db_user = db.query(Usuario).filter(Usuario.rut == user_rut).first()
    if not db_user:
        return None

    # Actualizar campos básicos
    if user.nombres is not None:
        db_user.nombres = user.nombres
    if user.apellidos is not None:
        db_user.apellidos = user.apellidos
    if user.correo is not None:
        db_user.correo = user.correo
    if user.telefono is not None:
        db_user.telefono = user.telefono
    if user.fecha_nacimiento is not None:
        db_user.fecha_nacimiento = user.fecha_nacimiento

    # Actualizar contraseña solo si se proporciona
    if user.password:  # Cambiado de hashed_password a password
        db_user.hashed_password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user
#FUNCIONES PARA USUARIOS NORMALES


#FUNCIONES COMPLEMENTARIAS
#Función que obtiene un usuario por su RUT
def get_user_by_rut(db: Session, user_rut: str):
    return db.query(Usuario).filter(Usuario.rut == user_rut).first()

#Función que obtiene un usuario por su ID
def get_user_by_rut(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

#Función que obtiene un usuario por su nombre (DEBERIA SER POR CORREO)
def get_user_by_nombres(db: Session, nombres: str):
    return db.query(Usuario).filter(Usuario.nombres == nombres).first()
#FUNCIONES COMPLEMENTARIAS