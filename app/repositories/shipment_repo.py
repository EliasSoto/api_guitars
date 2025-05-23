from sqlalchemy.orm import Session
from app.models.shipment import Shipment
from app.models.shipment_detail import ShipmentDetail
from app.models.order import Order
from fastapi import HTTPException, status
from app.schemas.shipment import ShipmentListResponse
from typing import Optional

### FUNCIONES PARA GESTIÓN DE ENVÍOS ###

# Función para crear un nuevo envío.
def create_shipment(db: Session, order_id: int, shipment_data: dict):
    try:
        # Verifica si el pedido existe
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        # Crea el envío (usa shipment_data["campo"] para acceder a los valores)
        db_shipment = Shipment(
            shipment_date=shipment_data["shipment_date"],  # Acceso como dict
            tracking_status=shipment_data["tracking_status"],
            delivery_date=shipment_data.get("delivery_date"),  # Usa .get() para campos opcionales
            price=shipment_data["price"],
            shipping_provider=shipment_data["shipping_provider"],
            is_immediate_delivery=shipment_data["is_immediate_delivery"],
            order_id=order_id
        )
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)

        # Crea la relación con el pedido
        shipment_detail = ShipmentDetail(
            tracking_number_id=db_shipment.id,
            order_id=order_id
        )
        
        db.add(shipment_detail)
        db.commit()

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
        Shipment.id == shipment_detail.tracking_number_id
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
        ShipmentDetail.tracking_number_id == shipment_id
    ).delete()

    # Luego eliminamos el envío
    db.delete(db_shipment)
    db.commit()
    return db_shipment

# Función para obtener envíos paginados.
def get_user_shipments_paginated(db: Session, user_id: int, page: int, limit: int):
    offset = (page - 1) * limit

    # Consulta base con joins necesarios
    query = db.query(Shipment).join(ShipmentDetail).join(Order).filter(
        Order.user_id == user_id
    )
    
    # Obtener los envíos paginados
    shipments = query.offset(offset).limit(limit).all()
    
    # Contar el total
    total = query.count()

    # Devuelve siempre un ShipmentListResponse válido
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