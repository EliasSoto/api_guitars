from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas import usuario as usuario_schema
from core.utils import hash_password, verify_password

def create_user_by_admin(db: Session, user: usuario_schema.UsuarioCreateByAdmin):
    hashed_password = hash_password(user.password)  # Hasheamos la contraseña antes de guardarla  
    db_user = Usuario(
        rut=user.rut,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        password=hashed_password,  # Nueva contraseña hasheada
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento,
        es_administrador=user.es_administrador
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: usuario_schema.UsuarioCreate):
    hashed_password = hash_password(user.password)  # Hasheamos la contraseña antes de guardarla  
    db_user = Usuario(
        rut=user.rut,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        password=hashed_password,  # Nueva contraseña hasheada
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento,
        es_administrador=False  # El valor por defecto es False para usuarios normales
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user