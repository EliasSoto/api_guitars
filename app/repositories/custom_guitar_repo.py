from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.custom_guitar import CustomGuitar
from app.models.guitar import Guitar
from app.models.component import Component
from app.repositories import component_detail_repo
from app.schemas import custom_guitar as custom_guitar_schema
from app.models.component_detail import ComponentDetail
from app.schemas.custom_guitar import ComponentDetailCreate, CustomGuitarListResponse, CustomGuitarCreate


# Crear una guitarra personalizada basada en un modelo y lista de componentes
def create_custom_guitar(
    db: Session,
    user_id: int,
    data: CustomGuitarCreate
):
    # Validar guitarra base
    base_guitar = db.query(Guitar).filter(Guitar.id == data.guitar_id).first()
    if not base_guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra base no encontrada."
        )

    final_price = base_guitar.sale_price or 0.0

    custom_guitar = CustomGuitar(
        guitar_id=data.guitar_id,
        user_id=user_id,
        total_price=0.0,
        custom_color=data.custom_color,
        custom_fret=data.custom_fret,
        jack_position=data.jack_position
    )
    db.add(custom_guitar)
    db.commit()
    db.refresh(custom_guitar)

    for detail in data.component_details:
        component = db.query(Component).filter(
            Component.id == detail.component_id
        ).with_for_update().first()

        if not component:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Componente ID {detail.component_id} no encontrado"
            )

        if component.stock is None or component.stock < detail.quantity:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el componente ID {detail.component_id}"
            )
        
        # Actualizar stock del componente
        component.stock -= detail.quantity
        db.add(component)

        unit_price = component.sale_price or 0.0
        subtotal = unit_price * detail.quantity
        final_price += subtotal
        # Crear y agregar el ComponentDetail
        component_detail = ComponentDetail(
            custom_guitar_id=custom_guitar.id,
            component_id=detail.component_id,
            quantity=detail.quantity,
            unit_price=unit_price
        )
        db.add(component_detail)

    # Actualizar el total de la guitarra personalizada
    custom_guitar.total_price = final_price
    db.commit()
    db.refresh(custom_guitar)

    return custom_guitar

# Obtener las guitarras personalizadas del usuario autenticado
def get_custom_guitars_paginated_user(db: Session, user_id: int, page: int, limit: int):
    offset = (page - 1) * limit

    guitars = (
        db.query(CustomGuitar)
        .filter(CustomGuitar.user_id == user_id)
        .order_by(CustomGuitar.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(CustomGuitar).filter(CustomGuitar.user_id == user_id).count()

    if not guitars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras personalizadas en esta página."
        )

    return CustomGuitarListResponse(guitars=guitars, total=total)

# Eliminar una guitarra personalizada
def delete_custom_guitar(db: Session, custom_guitar_id: int):
    custom = db.query(CustomGuitar).filter(CustomGuitar.id == custom_guitar_id).first()
    if not custom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra personalizada no encontrada."
        )
    db.delete(custom)
    db.commit()
    return custom

# Obtener todas las guitarras personalizadas (Admin)
def get_all_custom_guitars_paginated_admin(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    guitars = (
        db.query(CustomGuitar)
        .order_by(CustomGuitar.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(CustomGuitar).count()

    if not guitars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras personalizadas en esta página."
        )

    return CustomGuitarListResponse(guitars=guitars, total=total)