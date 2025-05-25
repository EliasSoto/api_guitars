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

# Función para obtener una guitarra por id.
def get_guitar_by_id(db: Session, guitar_id: int):
    db_guitar = db.query(Guitar).filter(Guitar.id == guitar_id).first()
    if not db_guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra no encontrada"
        )
        
    return db_guitar

# Función para obtener guitarras paginadas.
def get_guitars_paginated(db: Session, page: int, limit: int):
    # Calculamos el offset basado en la página y el límite.
    offset = (page - 1) * limit

    # Consultamos las guitarras con el offset y el limit.
    guitars = db.query(Guitar).offset(offset).limit(limit).all()

    # Consultamos el total de guitarras.
    total_guitars = db.query(Guitar).count()

    # Si no se encuentran guitarras, lanzamos una excepción.
    if not guitars:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras en esta página."
        )

    # Devolvemos las guitarras junto con el total.
    return GuitarListResponse(guitars=guitars, total=total_guitars)