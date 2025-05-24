from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import order as order_schema
from repositories import order_repo
from database.session import get_db
from core.auth import verify_token
from typing import List

# Necesario para la creación de la API en MAIN.
router = APIRouter()

### ENDPOINTS PARA ADMINISTRADORES DE PEDIDOS ###


# Endpoint para obtener un pedido por id.
@router.get("/admin/pedidos/{order_id}", tags=["Pedidos Admin"], response_model=order_schema.OrderRead)
def read_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este pedido"
        )

    return order_repo.get_order_by_id(db=db, order_id=order_id)

# Endpoint para actualizar una ordenes por id.
@router.put("/admin/pedidos/{order_id}", tags=["Pedidos Admin"], response_model=order_schema.OrderRead)
def update_order_by_id(
    order_id: int,
    order: order_schema.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar pedidos"
        )

    return order_repo.update_order(db=db, order_id=order_id, order_data=order)
    
# Endpoint para eliminar una orden por parte de un administrador.
@router.delete("/admin/pedidos/{order_id}", tags=["Pedidos Admin"])
def delete_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este pedido"
        )
        
    return order_repo.delete_order(db=db, order_id=order_id)

### ENDPOINTS DE USUARIOS NORMALES ###

# Endpoint para obtener pedidos del usuario autenticado.
@router.get("/usuarios/pedidos", tags=["Pedidos Usuario"], response_model=List[order_schema.OrderRead])
def read_user_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    orders = order_repo.get_all_orders(db=db, user_id=current_user["id"])
    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes pedidos registrados"
        )
    return orders

# Endpoint para generar un pedido.
@router.post("/usuarios/pedidos", tags=["Pedidos Usuario"], response_model=order_schema.OrderRead)
def create_order(
    order: order_schema.OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    # Solo usuarios autenticados pueden crear pedidos
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden crear pedidos"
        )

    return order_repo.create_order(db=db, user_id=current_user["id"], order=order)