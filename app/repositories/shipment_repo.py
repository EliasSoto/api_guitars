from sqlalchemy.orm import Session
from app.models.shipment import Shipment
from app.models.shipment_detail import ShipmentDetail
from app.models.order import Order
from fastapi import HTTPException, status
from app.schemas.shipment import ShipmentListResponse
from typing import Optional
from datetime import date


### FUNCIONES PARA GESTIÓN DE ENVÍOS ###

# Función para crear un nuevo envío.
def create_shipment(db: Session, order_ids: list[int], user_id: int):
    try:
        # Verificar que todos los pedidos existan
        orders = db.query(Order).filter(Order.id.in_(order_ids)).all()
        if len(orders) != len(order_ids):
            raise HTTPException(
                status_code=404,
                detail="Uno o más pedidos no fueron encontrados"
            )

        # Crear el envío solo con tracking_status = procesando
        db_shipment = Shipment(
            shipment_date=None,
            tracking_status="procesando",
            delivery_date=None,
            price=None,
            shipping_provider=None,
            is_immediate_delivery=None,
            user_id=user_id
        )
        db.add(db_shipment)
        db.flush()

        # Crear detalles de envío para cada pedido
        for order_id in order_ids:
            shipment_detail = ShipmentDetail(
                shipment_id=db_shipment.id,
                order_id=order_id
            )
            db.add(shipment_detail)

        db.commit()
        db.refresh(db_shipment)

        return db_shipment

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear el envío: {str(e)}"
        )

# Función para obtener un envío por ID.
def get_shipment_by_id(db: Session, shipment_id: int):
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envío no encontrado"
        )
        
    return db_shipment

# Función para obtener un envío por ID de pedido.
def get_shipment_by_order_id(db: Session, order_id: int):
    # Obtener el detalle de envío para el pedido
    shipment_detail = db.query(ShipmentDetail).filter(
        ShipmentDetail.order_id == order_id
    ).first()
    
    if not shipment_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró envío para este pedido"
        )
    
    # Obtener la información completa del envío
    db_shipment = db.query(Shipment).filter(
        Shipment.id == shipment_detail.shipment_id
    ).first()
    
    return db_shipment

# Función para actualizar un envío por ID.
def update_shipment(db: Session, shipment_id: int, shipment_data: dict):
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envío no encontrado"
        )

    update_data = shipment_data.dict(exclude_unset=True)

    # Actualizamos los campos proporcionados
    for key, value in update_data.items():
        setattr(db_shipment, key, value)

    db.commit()
    db.refresh(db_shipment)
    return db_shipment

# Función para eliminar un envío por ID.
def delete_shipment(db: Session, shipment_id: int):
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envío no encontrado"
        )

    # Primero eliminamos los detalles de envío asociados
    db.query(ShipmentDetail).filter(
        ShipmentDetail.shipment_id == shipment_id
    ).delete()

    # Luego eliminamos el envío
    db.delete(db_shipment)
    db.commit()
    return db_shipment


def get_user_shipments_paginated(
    db: Session,
    page: int,
    limit: int,
    user_id: int = None,
    search: str = None,
    search_by: str = 'id'
):
    offset = (page - 1) * limit

    query = db.query(Shipment).order_by(Shipment.id.asc())

    if user_id is not None:
        query = query.filter(Shipment.user_id == user_id)

    if search:
        if search_by == "id":
            if search.isdigit():
                query = query.filter(Shipment.id == int(search))
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El ID debe ser un número entero válido."
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campo de búsqueda inválido. Solo se permite 'id'."
            )

    total = query.count()
    shipments = query.offset(offset).limit(limit).all()

    return ShipmentListResponse(
        shipments=shipments,
        total=total
    )

# Función para obtener todos los envíos paginados (para administradores).
def get_all_shipments_paginated(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    query = (
        db.query(Shipment)
        .join(ShipmentDetail)
        .join(Order)
        .order_by(Shipment.id.asc())
        .distinct()
    )

    total = query.count()
    shipments = query.offset(offset).limit(limit).all()

    return ShipmentListResponse(
        shipments=shipments,
        total=total
    )

# Función para actualizar el estado de un envío.
def update_shipment_status(db: Session, shipment_id: int, new_status: str):
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envío no encontrado"
        )

    db_shipment.tracking_status = new_status
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

# Función para obtener el ID de envío asociado a un pedido.
def get_shipment_id_by_order_id(db: Session, order_id: int) -> Optional[int]:
    result = db.query(ShipmentDetail).filter(ShipmentDetail.order_id == order_id).first()
    if result:
        return result.shipment_id
    return None