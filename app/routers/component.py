from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import component as component_schema
from repositories import component_repo
from database.session import get_db
from core.auth import verify_token
from typing import List

router = APIRouter()

# Crear componente (Admin)
@router.post("/admin/componentes", tags=["Componentes Admin"], response_model=component_schema.ComponentRead)
def create_component(
    component: component_schema.ComponentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear componentes")
    
    return component_repo.create_component(db=db, component=component)

# Actualizar componente por ID (Admin)
@router.put("/admin/componentes/{component_id}", tags=["Componentes Admin"], response_model=component_schema.ComponentRead)
def update_component(
    component_id: int,
    component: component_schema.ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar componentes")
    
    return component_repo.update_component(db=db, component_id=component_id, component_data=component)

# Eliminar componente por ID (Admin)
@router.delete("/admin/componentes/{component_id}", tags=["Componentes Admin"])
def delete_component(
    component_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar componentes")
    
    return component_repo.delete_component(db=db, component_id=component_id)

# Obtener componentes paginados (Admin)
@router.get("/admin/componentes", tags=["Componentes Admin"], response_model=component_schema.ComponentListResponse)
def get_components_paginated(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver componentes")
    
    return component_repo.get_components_paginated(db=db, page=page, limit=limit)