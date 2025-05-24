from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import guitar as guitar_schema
from repositories import guitar_repo
from database.session import get_db
from core.auth import verify_token
from typing import List

# Necesario para la creación de la API en MAIN.
router = APIRouter()

### ENDPOINTS PARA ADMINISTRADORES DE GUITARRAS ###

# Endpoint para crear una nueva guitarra por parte de un administrador.
@router.post("/admin/guitarras", tags=["Guitarras Admin"], response_model=guitar_schema.GuitarRead)
def create_guitar(
    guitar: guitar_schema.GuitarCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear guitarras"
        )
    
    new_guitar = guitar_repo.create_guitar(db=db, guitar=guitar)

    return new_guitar

# Endpoint para actualizar una guitarra por id.
@router.put("/admin/guitarras/{guitar_id}", tags=["Guitarras Admin"], response_model=guitar_schema.GuitarRead)
def update_guitar_by_id(
    guitar_id: int,
    guitar: guitar_schema.GuitarUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar guitarras"
        )

    return guitar_repo.update_guitar(db=db, guitar_id=guitar_id, guitar_data=guitar)
    

# Endpoint para eliminar una guitarra por parte de un administrador.
@router.delete("/admin/guitarras/{guitar_id}", tags=["Guitarras Admin"])
def delete_guitar_by_id(
    guitar_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar guitarras"
        )

    return guitar_repo.delete_guitar(db=db, guitar_id=guitar_id)

### ENDPOINTS DE USUARIOS NORMALES ###

# Endpoint para obtener una guitarra por id. (Endpoint público)
@router.get("/guitarras/{guitar_id}", tags=["Guitarras Públicas"], response_model=guitar_schema.GuitarRead)
def read_guitar_by_id(
    guitar_id: int,
    db: Session = Depends(get_db)
):
    return guitar_repo.get_guitar_by_id(db=db, guitar_id=guitar_id)

# Endpoint para obtener las guitarras paginadas. (Endpoint público)
@router.get("/guitarras", tags=["Guitarras Públicas"], response_model=guitar_schema.GuitarListResponse)
def get_paginated_guitars(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return guitar_repo.get_guitars_paginated(db=db, page=page, limit=limit)