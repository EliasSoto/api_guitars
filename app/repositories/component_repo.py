# app/repositories/component_repo.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.component import Component
from app.schemas import component as component_schema
from app.schemas.component import ComponentListResponse

### FUNCIONES PARA COMPONENTES ###

# Crear un nuevo componente
def create_component(db: Session, component: component_schema.ComponentCreate):
    db_component = Component(
        name=component.name,
        type=component.type,
        purchase_price=component.purchase_price,
        sale_price=component.sale_price,
        net_price=component.net_price,
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
def get_components_paginated(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    components = (
        db.query(Component)
        .order_by(Component.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_components = db.query(Component).count()

    if not components:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron componentes en esta página."
        )

    return ComponentListResponse(components=components, total=total_components)

# Obtener componentes paginados
def get_components_paginated_admin(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    components = (
        db.query(Component)
        .order_by(Component.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_components = db.query(Component).count()

    if not components:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron componentes en esta página."
        )

    return ComponentListResponse(components=components, total=total_components)

# Función para obtener guitarras paginadas con stock disponible.
def get_guitars_paginated_user(db: Session, page: int, limit: int):
    offset = (page - 1) * limit

    components = (
        db.query(Component)
        .order_by(Component.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_components = db.query(Component).filter(Component.stock > 0).count()

    if not components:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron componentes con stock en esta página."
        )

    return ComponentListResponse(components=components, total=total_components)
