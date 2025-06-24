from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from repositories import user_repo
from database.session import get_db
from core.auth import verify_token, verify_token_optional
from typing import List, Optional

# Necesario para la creación de la API en MAIN.
router = APIRouter()

# Endpoint para la raíz de la API. Oculto (false)
@router.get("/", tags=["Inicio"], include_in_schema=False)
def read_root():
    return {"message": "Bienvenido a la API de Proyecto Guitarras."}


### ENDPOINTS DE USUARIOS ADMINISTRADORES ###

# Endpoint para crear un nuevo usuario por parte de un administrador.
@router.post("/admin/usuarios", tags=["Usuarios Admin"], response_model=user_schema.UserRead)
def create_user(
    user: user_schema.UserCreateByAdmin,
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

# Endpoint para obtener una lista paginada de usuarios por parte de un administrador.
@router.get("/admin/usuarios", tags=["Usuarios Admin"], response_model=user_schema.UserListResponse)
def get_paginated_users(
    page: int = 1,
    limit: int = 10,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Se verifica que el usuario logueado sea admin.
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los usuarios"
        )
    
    return user_repo.get_users_paginated(db=db, page=page, limit=limit, search=search)

# Endpoint para obtener un usuario por id.
@router.get("/admin/usuarios/{user_id}", tags=["Usuarios Admin"], response_model=user_schema.UserRead)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Se verifica que el usuario logueado sea admin.
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver otros usuarios"
        )

    db_user = user_repo.get_user_by_id(db=db, user_id=user_id)

    # Se verifica que el usuario exista.
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return db_user

# Endpoint para actualizar un usuario por id.
@router.put("/admin/usuarios/{user_id}", tags=["Usuarios Admin"], response_model=user_schema.UserAdminRead)
def update_user_by_id(
    user_id: int,
    user: user_schema.UserUpdateByAdmin,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Se verifica que el usuario logueado sea admin.
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar usuarios"
        )

    db_user = user_repo.get_user_by_id(db=db, user_id=user_id)

    # Se verifica que el usuario exista.
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    # Se verifica que el usuario logueado no esté intentando actualizar su propio perfil.
    if current_user["id"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes modificar tu propio usuario."
        )

    # Se intenta actualizar el usuario y se maneja la excepción en caso de error.
    try:
        updated_user = user_repo.update_user_by_admin(db=db, user_id=user_id, user=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}"
        )
        
    return updated_user
    

# Endpoint para eliminar un usuario por parte de un administrador.
@router.delete("/admin/usuarios/{user_id}", tags=["Usuarios Admin"])
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Se verifica que el usuario logueado sea admin.
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar usuarios"
        )

    db_user = user_repo.get_user_by_id(db=db, user_id=user_id)

    # Se verifica que el usuario exista.
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    # Se verifica que el usuario no intente eliminar su propio perfil.
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes eliminarte a ti mismo"
        )

    # Se intenta eliminar el usuario y se maneja la excepción en caso de error.
    try:
        user_repo.delete_user_by_admin(db=db, user_id=user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}"
        )

    return {"message": "Usuario eliminado correctamente"}

# Endpoint para obtener el nombre completo de un usuario por id.
@router.get("/admin/usuarios/nombre/{user_id}/", tags=["Usuarios Admin"], response_model=user_schema.UserFullNameResponse)
def get_user_full_name_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Solo los administradores pueden acceder
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver esta información"
        )

    user = user_repo.get_user_by_id(db=db, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    full_name = f"{user.first_name} {user.last_name}"
    return {"full_name": full_name}

### ENDPOINTS DE USUARIOS NORMALES ###

# Endpoint para registrar un nuevo usuario normal. (Endpoint Público).
@router.post("/usuarios", tags=["Usuarios Normales"], response_model=user_schema.UserRead)
def register_normal_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: Optional[dict] = Depends(verify_token_optional)  
):
    # Se verifica si el usuario está logueado.
    if current_user:
        db_user = user_repo.get_user_by_id(db=db, user_id=current_user["id"])
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya tienes una cuenta registrada"
            )

    # Se intenta crear el usuario y se maneja la excepción en caso de error.
    try:
        new_user = user_repo.create_user(db=db, user=user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )

# Endpoint para actualizar un usuario normal logueado.
@router.put("/usuarios", tags=["Usuarios Normales"], response_model=user_schema.UserRead)
def update_normal_user(
    user_update: user_schema.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    try:
        updated_user = user_repo.update_normal_user(
            db=db,
            user_id=current_user["id"],
            user=user_update, 
            current_user_id=current_user["id"]
        )
        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el usuario: {str(e)}"
        )
        
# Endpoint para obtener el perfil del usuario normal logueado.
@router.get("/usuarios", tags=["Usuarios Normales"], response_model=user_schema.UserRead)
def read_normal_user(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    db_user = user_repo.get_user_by_id(db=db, user_id=current_user["id"])

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado:"
        )

    return db_user


