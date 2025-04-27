from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import address as address_schema
from repositories import user_repo, address_repo
from database.session import get_db
from core.auth import verify_token
from fastapi.responses import JSONResponse

# Necesario para la creación de la API en MAIN
router = APIRouter()

# Endpoint para crear la dirección activa del usuario autenticado
@router.post("/direcciones", tags=["Direcciones Usuarios"], response_model=address_schema.AddressRead)
def create_address(
    address: address_schema.AddressCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    
    # Verificamos si el usuario autenticado existe.
    db_user = user_repo.get_user_by_id(db=db, user_id=current_user["id"]) 
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Intentamos crear la dirección activa
    try:
        db_address = address_repo.create_address(db, db_user.id, address)
        return db_address
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ingresar la dirección actual: {str(e)}"
        )

# Endpoint para obtener todas las direcciones del usuario autenticado
@router.get("/direcciones", tags=["Direcciones Usuarios"], response_model=list[address_schema.AddressRead])
def read_all_addresses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    addresses = address_repo.get_all_addresses(db=db, user_id=current_user["id"])

    if not addresses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes direcciones registradas"
        )

    return addresses

# Endpoint para actualizar una dirección específica del usuario autenticado
@router.put("/direcciones/{address_id}", tags=["Direcciones Usuarios"], response_model=address_schema.AddressRead)
def update_user_address(
    address_id: int,
    address: address_schema.AddressUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Obtenemos el usuario autenticado
    db_user = user_repo.get_user_by_id(db=db, user_id=current_user["id"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Intentamos actualizar la dirección
    try:
        updated_adress = address_repo.update_address(
            db=db,
            user_id=db_user.id,
            address_id=address_id,
            address_data=address
        )
        return updated_adress
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la dirección: {str(e)}"
        )

# Endpoint para eliminar una dirección específica del usuario autenticado
@router.delete("/direcciones/{address_id}", tags=["Direcciones Usuarios"])
def delete_user_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Obtenemos el usuario autenticado
    db_user = user_repo.get_user_by_id(db=db, user_id=current_user["id"])
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Intentamos eliminar la dirección
    try:
        content = address_repo.delete_address_by_id(
            db=db,
            user_id=db_user.id,
            address_id=address_id
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la dirección: {str(e)}"
        )
