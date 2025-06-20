# app/repositories/component_repo.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.component import Component
from app.schemas import component as component_schema
from app.schemas.component import ComponentListResponse

### FUNCIONES PARA COMPONENTES ###

# Crear un nuevo componente
def create_component(db: Session, component: component_schema.ComponentCreate):
    net_price = int(round(component.sale_price / 1.19, 0))
    
    db_component = Component(
        name=component.name,
        type=component.type,
        purchase_price=component.purchase_price,
        sale_price=component.sale_price,
        net_price=net_price,
        stock=component.stock,
        description=component.description,
        purchase_date=component.purchase_date,
        brand=component.brand,
        material=component.material,
        position=component.position,
        is_active=component.is_active if component.is_active is not None else True
    )
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

# Obtener todos los componentes
def get_all_components(db: Session):
    return db.query(Component).all()

# Obtener un componente por ID
def get_component_by_id(db: Session, component_id: int):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if not db_component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Componente no encontrado"
        )
    return db_component

# Actualizar un componente por ID
def update_component(db: Session, component_id: int, component_data: component_schema.ComponentUpdate):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if not db_component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Componente no encontrado"
        )

    update_data = component_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_component, key, value)
        
    # Se recalcula net_price se actualiza uel sale_price
    price_base = update_data.get("sale_price")
    if price_base:
        net_price = int(round(price_base / 1.19, 0))
        db_component.net_price = net_price

    db.commit()
    db.refresh(db_component)
    return db_component

# Eliminar un componente por ID
def delete_component(db: Session, component_id: int):
    db_component = db.query(Component).filter(Component.id == component_id).first()
    if not db_component:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Componente no encontrado"
        )

    db.delete(db_component)
    db.commit()
    return db_component

# Obtener componentes paginados
def get_components_paginated_filtered(db: Session, page: int, limit: int, stock_only: bool = False):
    offset = (page - 1) * limit
    query = db.query(Component)
    
    if stock_only:
        query = query.filter(Component.stock > 0)

    components = query.order_by(Component.id.asc()).offset(offset).limit(limit).all()
    total = query.count()

    if not components:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron componentes en esta página."
        )

    return ComponentListResponse(components=components, total=total)

# Función para obtener componentes por tipo, subtipo y estado activo
def get_components_by_type_subtype_active(db: Session, page: int, limit: int, type: str = None, subtype: str = None, is_active: bool = None, stock_only: bool = False):
    offset = (page - 1) * limit

    query = db.query(Component)

    if type:
        query = query.filter(Component.type == type)
    if subtype:
        query = query.filter(Component.subtype == subtype)
    if is_active is not None:
        query = query.filter(Component.is_active == is_active)
    if stock_only:
        query = query.filter(Component.stock > 0)

    total = query.count()
    components = query.offset(offset).limit(limit).all()

    if not components:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron componentes con los filtros especificados."
        )

    return ComponentListResponse(components=components, total=total)