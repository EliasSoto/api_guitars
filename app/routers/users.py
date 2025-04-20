# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from schemas import usuario as usuario_schema
# from repositories import user_repo
# from database.session import get_db
# from core.auth import verify_token

# router = APIRouter()

# @router.get("/", tags=["Inicio"])
# def read_root():
#     return {"message": "Bienvenido a la API de personalización de guitarras 🎸"}


# @router.post("/usuarios", tags=["Usuarios"])
# def create_user(
#     user: usuario_schema.UsuarioCreateByAdmin,  # Recibimos los datos del usuario
#     db: Session = Depends(get_db),  # Dependencia para obtener la sesión de la base de datos
#     current_user: dict = Depends(verify_token)  # Verificamos que el usuario esté autenticado
# ):
#     if current_user["role"] != "admin":  # Solo el admin puede crear usuarios
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para crear usuarios")
    
#     # Llamamos a la función que maneja la creación del usuario
#     new_user = user_repo.create_user_by_admin(db=db, user=user)
#     return {"message": "Usuario creado correctamente", "user": new_user}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import usuario as usuario_schema
from repositories import user_repo
from database.session import get_db
from core.auth import verify_token

router = APIRouter()

@router.get("/", tags=["Inicio"])
def read_root():
    return {"message": "Bienvenido a la API de personalización de guitarras 🎸"}

@router.post("/usuarios", tags=["Usuarios"])
def create_user(
    user: usuario_schema.UsuarioCreateByAdmin,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear usuarios"
        )

    new_user = user_repo.create_user_by_admin(db=db, user=user)

    return {
        "message": "Usuario creado correctamente",
        "user": {
            "id": new_user.id,
            "rut": new_user.rut,
            "nombres": new_user.nombres,
            "apellidos": new_user.apellidos,
            "correo": new_user.correo,
            "telefono": new_user.telefono,
            "fecha_nacimiento": new_user.fecha_nacimiento,
            "es_administrador": new_user.es_administrador
        }
    }
