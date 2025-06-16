from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import custom_guitar as custom_schema
from repositories import custom_guitar_repo
from database.session import get_db
from core.auth import verify_token
from typing import List
from fastapi import Query

router = APIRouter()

# Crear una guitarra personalizada (Usuario)
@router.post("/usuarios/guitarras-personalizadas", tags=["Guitarras Personalizadas Usuario"], response_model=custom_schema.CustomGuitarRead)
def create_custom_guitar(
    custom_guitar: custom_schema.CustomGuitarCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Solo los usuarios pueden crear guitarras personalizadas")

    return custom_guitar_repo.create_custom_guitar(
        db=db,
        user_id=current_user["id"],
        guitar_id=custom_guitar.guitar_id,
        total_price=0.0,
        component_details=custom_guitar.component_details
    )

# Obtener guitarras personalizadas del usuario autenticado
@router.get("/guitarras-personalizadas", response_model=custom_schema.CustomGuitarListResponse, tags=["Guitarras Personalizadas Usuario"])
def get_custom_guitars_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    return custom_guitar_repo.get_custom_guitars_paginated_user(db=db, user_id=current_user["id"], page=page, limit=limit)

# Obtener todas las guitarras personalizadas (Admin)
@router.get("/admin/guitarras-personalizadas", response_model=custom_schema.CustomGuitarListResponse, tags=["Guitarras Personalizadas Admin"])
def get_all_custom_guitars_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    return custom_guitar_repo.get_all_custom_guitars_paginated_admin(db=db, page=page, limit=limit)