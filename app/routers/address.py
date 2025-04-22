from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.direccion import DireccionCreate, DireccionRead
from repositories.address_repo import create_address, get_all_addresses, update_address, delete_address_by_id
from repositories import user_repo
from database.session import get_db
from core.auth import verify_token
from models.usuario import Usuario
from fastapi.responses import JSONResponse

router = APIRouter()

# Endpoint para crear la dirección activa del usuario autenticado
@router.post("/usuarios/me/direccion/activa", tags=["Direcciones Usuarios"], response_model=DireccionRead)
def create_adress(
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    
    # Verificamos si el usuario autenticado es el mismo que el de la ruta
    db_user = user_repo.get_user_by_rut(db=db, user_rut=current_user["rut"]) 
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Intentamos crear la dirección activa
    try:
        db_direccion = create_address(db, db_user.id, direccion)
        return db_direccion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ingresar la dirección actual: {str(e)}"
        )

# Endpoint para obtener todas las direcciones del usuario autenticado
@router.get("/usuarios/me/direccion", tags=["Direcciones Usuarios"], response_model=list[DireccionRead])
def read_all_addresses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    direcciones = get_all_addresses(db=db, user_id=current_user["id"])

    if not direcciones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes direcciones registradas"
        )

    return direcciones

# Endpoint para actualizar una dirección específica del usuario autenticado
@router.put("/usuarios/direccion/{direccion_id}", response_model=DireccionRead, tags=["Direcciones Usuarios"])
def update_user_address(
    direccion_id: int,
    direccion: DireccionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Obtenemos el usuario autenticado
    db_user = user_repo.get_user_by_rut(db=db, user_rut=current_user["rut"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Intentamos actualizar la dirección
    try:
        direccion_actualizada = update_address(
            db=db,
            user_id=db_user.id,
            direccion_id=direccion_id,
            direccion_data=direccion
        )
        return direccion_actualizada
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la dirección: {str(e)}"
        )

# Endpoint para eliminar una dirección específica del usuario autenticado
@router.delete("/usuarios/direccion/{direccion_id}", tags=["Direcciones Usuarios"])
def delete_user_address(
    direccion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Obtenemos el usuario autenticado
    db_user = user_repo.get_user_by_rut(db=db, user_rut=current_user["rut"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Intentamos eliminar la dirección
    try:
        result = delete_address_by_id(
            db=db,
            user_id=db_user.id,
            direccion_id=direccion_id
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la dirección: {str(e)}"
        )
