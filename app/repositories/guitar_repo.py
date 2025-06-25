from sqlalchemy.orm import Session
from app.models.guitar import Guitar
from fastapi import HTTPException, status
from app.schemas import guitar as guitar_schema
from app.schemas.guitar import GuitarListResponse

### FUNCIONES PARA USUARIOS ADMIN ###

# Función para crear una nueva guitarra.
def create_guitar(db: Session, guitar: guitar_schema.GuitarCreate):
    net_price = int(round(guitar.sale_price / 1.19, 0))
    iva = int(round(guitar.sale_price - net_price, 0))
    
    db_guitar = Guitar(
        model=guitar.model,
        brand=guitar.brand,
        description=guitar.description,
        purchase_price=guitar.purchase_price,
        sale_price=guitar.sale_price,
        net_price=net_price,
        iva=iva,
        purchase_date=guitar.purchase_date,
        wood_type=guitar.wood_type,
        image_link=guitar.image_link,
        color=guitar.color,
        stock=guitar.stock,
        is_custom=guitar.is_custom,
        fret_count=guitar.fret_count,
    )

    db.add(db_guitar)
    db.commit()
    db.refresh(db_guitar)
    
    return db_guitar

# Función para obtener todos las guitarras.
def get_all_guitar(db: Session):
    return db.query(Guitar).all()

# Función para actualizar una guitarra por id.
def update_guitar(db: Session, guitar_id: int, guitar_data: guitar_schema.GuitarUpdate):
    db_guitar = db.query(Guitar).filter(Guitar.id == guitar_id).first()
    if not db_guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra no encontrada"
        )

    update_data = guitar_data.dict(exclude_unset=True)

    # Actualizamos todos los campos proporcionados en guitar_data
    for key, value in update_data.items():
        setattr(db_guitar, key, value)
        
    # Se recalcula net_price e iva si hay un sale_price o liquidation_price
    price_base = update_data.get("liquidation_price") or update_data.get("sale_price")
    if price_base:
        net_price = int(round(price_base / 1.19, 0))
        iva = int(round(price_base - net_price, 0))
        db_guitar.net_price = net_price
        db_guitar.iva = iva

    # Se guardan los datos en la base de datos.
    db.commit()
    db.refresh(db_guitar)
    return db_guitar

# Función para eliminar un usuario por id.
def delete_guitar(db: Session, guitar_id: int):
    db_guitar = db.query(Guitar).filter(Guitar.id == guitar_id).first()
    if not db_guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra no encontrada"
        )

    # Se elimina el usuario de la base de datos.
    db.delete(db_guitar)
    db.commit()
    return db_guitar

# Función para obtener guitarra por madera (para personalización)
def get_guitar_by_wood(db: Session, wood_type: str):
    db_guitar = db.query(Guitar).filter(
        Guitar.wood_type == wood_type,
        Guitar.stock > 0
    ).first()

    if not db_guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró una guitarra con esa combinación."
        )
        
    return {"id": db_guitar.id}

# Función para obtener una guitarra por id.
def get_guitar_by_id(db: Session, guitar_id: int):
    db_guitar = db.query(Guitar).filter(Guitar.id == guitar_id).first()
    if not db_guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra no encontrada"
        )
        
    return db_guitar

# Función para obtener guitarras paginadas para admin.
def get_guitars_paginated_admin(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    guitars = (
        db.query(Guitar)
        .order_by(Guitar.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_guitars = db.query(Guitar).count()

    if not guitars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras en esta página."
        )

    return GuitarListResponse(guitars=guitars, total=total_guitars)


# Función para obtener guitarras paginadas con stock disponible.
def get_guitars_paginated_user(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    guitars = (
        db.query(Guitar)
        .filter((Guitar.stock > 0) & (Guitar.is_custom == False))
        .order_by(Guitar.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_guitars = db.query(Guitar).filter(Guitar.stock > 0).count()

    if not guitars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras con stock disponible en esta página."
        )

    return GuitarListResponse(guitars=guitars, total=total_guitars)

