from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas import usuario as usuario_schema
from core.utils import hash_password, verify_password

#Funciones que se ocupan para el crud del admin
def create_user_by_admin(db: Session, user: usuario_schema.UsuarioCreateByAdmin):
    hashed_password = hash_password(user.hashed_password)  # Hasheamos la contraseña antes de guardarla  
    db_user = Usuario(
        rut=user.rut,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        hashed_password=hashed_password,  # Nueva contraseña hasheada
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento,
        es_administrador=user.es_administrador
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session):
    return db.query(Usuario).all()

def get_user_by_rut(db: Session, user_rut: str):
    return db.query(Usuario).filter(Usuario.rut == user_rut).first()

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

def delete_user_by_admin(db: Session, user_rut: str):
    db_user = db.query(Usuario).filter(Usuario.rut == user_rut).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user
#Funciones que se ocupan para el crud del admin



#funcion que obitiene un usuario por su nombre
#Funcion utilizada para el login (auth.py)
def get_user_by_nombres(db: Session, nombres: str):
    return db.query(Usuario).filter(Usuario.nombres == nombres).first()





#Funciones para USUARIOS NORMALES
def create_user(db: Session, user: usuario_schema.UsuarioCreate):
    hashed_password = hash_password(user.password)  # Hasheamos la contraseña antes de guardarla  
    db_user = Usuario(
        rut=user.rut,
        nombres=user.nombres,
        apellidos=user.apellidos,
        correo=user.correo,
        hashed_password=hashed_password,  # Nueva contraseña hasheada
        telefono=user.telefono,
        fecha_nacimiento=user.fecha_nacimiento,
        es_administrador=False  # El valor por defecto es False para usuarios normales
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





#Funciones para USUARIOS NORMALES