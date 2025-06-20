from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import component as component_schema
from repositories import component_repo
from database.session import get_db
from core.auth import verify_token
from typing import List

router = APIRouter()

### ENDPOINTS PARA ADMINISTRADORES DE COMPONENTES ###

# Crear componente
@router.post("/admin/componentes", tags=["Componentes Admin"], response_model=component_schema.ComponentRead)
def create_component(
    component: component_schema.ComponentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para crear componentes")
    
    return component_repo.create_component(db=db, component=component)

# Actualizar componente por ID
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

# Eliminar componente por ID
@router.delete("/admin/componentes/{component_id}", tags=["Componentes Admin"])
def delete_component(
    component_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar componentes")
    
    return component_repo.delete_component(db=db, component_id=component_id)

# Obtener componentes paginados 
@router.get("/admin/componentes", tags=["Componentes Admin"], response_model=component_schema.ComponentListResponse)
def get_components_paginated(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver componentes")
    
    return component_repo.get_components_paginated_filtered(db=db, page=page, limit=limit, stock_only=False)

### ENDPOINTS PARA USUARIOS DE COMPONENTES ###

# Obtener componente por ID
@router.get("/usuario/componentes/{component_id}", tags=["Componentes Usuario"], response_model=component_schema.ComponentRead)
def get_component_by_id(
    component_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):    
    return component_repo.get_component_by_id(db=db, component_id=component_id)

# Obtener componentes paginados
@router.get("/usuario/componentes", tags=["Componentes Usuario"], response_model=component_schema.ComponentListResponse)
def get_components_paginated(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver componentes")
    
    return component_repo.get_components_paginated_filtered(db=db, page=page, limit=limit, stock_only=True)

# Obtener componentes por tipo y subtipo
@router.get("/usuario/componentes/filtrar", tags=["Componentes Usuario"], response_model=component_schema.ComponentListResponse)
def get_filtered_components_user(
    type: str = None,
    subtype: str = None,
    is_active: bool = None,
    stock_only: bool = True,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="No tienes permisos para ver componentes")
    
    return component_repo.get_components_by_type_subtype_active( db=db, page=page, limit=limit, type=type, subtype=subtype, is_active=is_active, stock_only=stock_only)

