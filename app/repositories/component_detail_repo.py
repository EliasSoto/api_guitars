from sqlalchemy.orm import Session
from app.models.component_detail import ComponentDetail

# Crear una relación entre una guitarra personalizada y un componente.
def add_component_to_custom_guitar(
    db: Session, custom_guitar_id: int, component_id: int, unit_price: float
):
    component_detail = ComponentDetail(
        custom_guitar_id=custom_guitar_id,
        component_id=component_id,
        unit_price=unit_price
    )
    db.add(component_detail)
    return component_detail

# Obtener todos los componentes de una guitarra personalizada.
def get_components_by_custom_guitar(db: Session, custom_guitar_id: int):
    return db.query(ComponentDetail).filter(
        ComponentDetail.custom_guitar_id == custom_guitar_id
    ).all()
