from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import usuario as usuario_schema
from repositories import user_repo
from database.session import get_db
from core.auth import verify_token, verify_token_optional
from typing import List, Optional
from schemas.usuario import UsuarioRead

# Necesario para la creación de la API en MAIN
router = APIRouter()

#Endpoint para la raíz de la API. Oculto (false)
@router.get("/", tags=["Inicio"], include_in_schema=False)
def read_root():
    return {"message": "Bienvenido a la API de Proyecto Guitarras."}


#ENDPOINTS DE USUARIOS ADMINISTRADORES

# Endpoint para crear un nuevo usuario por parte de un administrador.
@router.post("/admin/usuarios", tags=["Usuarios Admin"], response_model=usuario_schema.UsuarioRead)
def create_users(
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

    return new_user

#Endpoint para obtener todos los usuarios (solo admin).
@router.get("/admin/usuarios", tags=["Usuarios Admin"], response_model=List[UsuarioRead])
def read_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los usuarios"
        )

    return user_repo.get_all_users(db=db)   

# Endpoint para actualizar un usuario por parte de un administrador.
@router.put("/admin/usuarios/{user_rut}", tags=["Usuarios Admin"], response_model=usuario_schema.UsuarioRead)
def update_user(
    user_rut: str,
    user: usuario_schema.UsuarioUpdateByAdmin,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar usuarios"
        )

    db_user = user_repo.get_user_by_rut(db=db, user_rut=user_rut)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    try:
        updated_user = user_repo.update_user_by_admin(db=db, user_rut=user_rut, user=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}"
        )

    return updated_user

# Endpoint para eliminar un usuario por parte de un administrador.
@router.delete("/admin/usuarios/{user_rut}", tags=["Usuarios Admin"])
def delete_user(
    user_rut: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar usuarios"
        )

    db_user = user_repo.get_user_by_rut(db=db, user_rut=user_rut)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    try:
        user_repo.delete_user_by_admin(db=db, user_rut=user_rut)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}"
        )

    return {"message": "Usuario eliminado correctamente"}

# Endpoint para obtener un usuario por id
@router.get("/admin/usuarios/{user_id}", tags=["Usuarios Admin"], response_model=usuario_schema.UsuarioRead)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver usuarios"
        )

    db_user = user_repo.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return db_user

#ENDPOINTS DE USUARIOS ADMINISTRADORES


#ENDPOINTS DE USUARIOS NORMALES

#ENDPOINT PUBLICO, Se verfiica el token de manera opcional porque si no tengo cuenta no tengo token.
#Registro de un nuevo usuario normal que no tiene cuenta.
@router.post("/usuarios", tags=["Usuarios Normales"], response_model=usuario_schema.UsuarioRead)
def register_user(
    user: usuario_schema.UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(verify_token_optional)  
):
    if current_user:
        print("Usuario autenticado:", current_user)
        # si quieres restringir que no se registren de nuevo si ya tienen cuenta
        db_user = user_repo.get_user_by_rut(db=db, user_rut=current_user["rut"])
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya tienes una cuenta"
            )

    # Crear usuario nuevo
    try:
        new_user = user_repo.create_user(db=db, user=user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear usuario: {str(e)}"
        )

# Endpoint para actualizar un usuario normal logueado.
@router.put("/usuarios", tags=["Usuarios Normales"], response_model=usuario_schema.UsuarioRead)
def update_normal_user(
    user_update: usuario_schema.UsuarioUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    try:
        updated_user = user_repo.update_normal_user(
            db=db,
            user_rut=current_user["rut"],
            user=user_update, 
            current_user_rut=current_user["rut"]
        )
        return updated_user
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}"
        )
        
# Endpoint para obtener el perfil del usuario normal logueado.
@router.get("/usuarios", tags=["Usuarios Normales"], response_model=usuario_schema.UsuarioRead)
def get_normal_user(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    db_user = user_repo.get_user_by_rut(db=db, user_rut=current_user["rut"])

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return db_user

#ENDPOINTS DE USUARIOS NORMALES


