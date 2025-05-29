from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import shipment as shipment_schema
from repositories import shipment_repo
from database.session import get_db
from core.auth import verify_token
from typing import List
from app.models.order import Order

# Necesario para la creación de la API en MAIN.
router = APIRouter()

### ENDPOINTS PARA ADMINISTRADORES DE ENVIO ###

# Endpoint para que el admin obtenga todos los envíos paginados
@router.get("/admin/envios", tags=["Envíos Admin"], response_model=shipment_schema.ShipmentListResponse)
def get_all_shipments_paginated(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los envíos"
        )

    response = shipment_repo.get_all_shipments_paginated(db=db, page=page, limit=limit)

    if not response.shipments or response.total == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay envíos registrados"
        )

    return response

# Endpoint para obtener un envio por id.
@router.get("/admin/envios/{shipment_id}", tags=["Envíos Admin"], response_model=shipment_schema.ShipmentRead)
def read_shipment_by_id(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este envío"
        )

    return shipment_repo.get_shipment_by_id(db=db, shipment_id=shipment_id)

# Endpoint para actualizar un envio por id.
@router.put("/admin/envios/{shipment_id}", tags=["Envíos Admin"], response_model=shipment_schema.ShipmentRead)
def update_shipment_by_id(
    shipment_id: int,
    shipment: shipment_schema.ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar envíos"
        )

    return shipment_repo.update_shipment(db=db, shipment_id=shipment_id, shipment_data=shipment)
    
# Endpoint para eliminar un pedido por parte de un administrador.
@router.delete("/admin/envios/{shipment_id}", tags=["Envíos Admin"])
def delete_shipment_by_id(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este envío"
        )
        
    return shipment_repo.delete_shipment(db=db, shipment_id=shipment_id)

### ENDPOINTS DE USUARIOS NORMALES ###

# Endpoint para obtener envios del usuario autenticado.
@router.get("/usuarios/envios", tags=["Envíos Usuario"], response_model=shipment_schema.ShipmentListResponse)
def get_user_shipments_paginated(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Obtener la respuesta paginada
    response = shipment_repo.get_user_shipments_paginated(
        db=db,
        user_id=current_user["id"],
        page=page,
        limit=limit
    )
    
    # Verificar si no hay envíos
    if not response.shipments or response.total == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes envíos registrados"
        )
    
    return response

# Endpoint para generar un pedido.
@router.post("/usuarios/envios", tags=["Envíos Usuario"], response_model=shipment_schema.ShipmentRead)
def create_shipment(
    shipment: shipment_schema.ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden crear envíos"
        )

    return shipment_repo.create_shipment( db=db, order_ids=shipment.order_ids, user_id=current_user["id"], shipment_data=shipment.dict(exclude={"order_ids"} )
    )