from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import order as order_schema
from repositories import order_repo
from database.session import get_db
from core.auth import verify_token
from app.schemas.guitar import GuitarSimpleRead
from typing import List
from typing import Optional

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

# Endpoint para que el admin obtenga todos los pedidos paginados
@router.get("/admin/pedidos", tags=["Pedidos Admin"], response_model=order_schema.OrderListResponse)
def get_all_orders_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = None,
    search_by: str = "id",
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver todos los pedidos"
        )

    response = order_repo.get_all_orders_paginated(
        db=db, page=page, limit=limit, search=search, search_by=search_by
    )

    if not response.orders or response.total == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay pedidos registrados"
        )

    return response


### ENDPOINTS DE USUARIOS NORMALES ###
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

# Endpoint para obtener todas las guitarras que el usuario ha pedido
@router.get("/usuarios/pedidos/guitarras", tags=["Pedidos Usuario"], response_model=List[GuitarSimpleRead])
def get_guitars_from_user_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden consultar sus guitarras pedidas"
        )

    return order_repo.get_user_ordered_guitars(db=db, user_id=current_user["id"])

# Endpoint para obtener pedidos paginados del usuario autenticado
@router.get("/usuarios/pedidos/", tags=["Pedidos Usuario"], response_model=order_schema.OrderListResponse)
def get_user_orders_paginated(
    page: int = 1,
    limit: int = 10,
    is_custom: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden consultar sus pedidos"
        )

    return order_repo.get_orders_paginated(
        db=db,
        page=page,
        limit=limit,
        user_id=current_user["id"],
        is_custom=is_custom
    )


# Endpoint para obtener un pedido por id.
@router.get("/usuarios/pedidos/{order_id}", tags=["Pedidos Usuario"], response_model=order_schema.OrderRead)
def read_order_by_id_usuario(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    order = order_repo.get_order_by_id(db=db, order_id=order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    if order.user_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este pedido"
        )

    return order