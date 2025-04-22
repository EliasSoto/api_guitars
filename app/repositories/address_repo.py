from sqlalchemy.orm import Session
from models.direccion import Direccion
from schemas.direccion import DireccionCreate
from fastapi import HTTPException, status

# Crear una nueva dirección
def create_address(db: Session, user_id: int, direccion: DireccionCreate):
    # Siempre que se crea una nueva, se inactivan las anteriores
    db.query(Direccion).filter(
        Direccion.id_usuario == user_id,
        Direccion.es_activa == True
    ).update({"es_activa": False})

    # Se crea una nueva dirección forzadamente activa
    nueva_direccion = Direccion(
        numero_calle=direccion.numero_calle,
        region=direccion.region,
        comuna=direccion.comuna,
        indicaciones=direccion.indicaciones,
        tipo_domicilio=direccion.tipo_domicilio,
        id_usuario=user_id,
        es_activa=True
    )

    db.add(nueva_direccion)
    db.commit()
    db.refresh(nueva_direccion)

    return nueva_direccion

# Actualizar una dirección específica por ID
def update_address(db: Session, user_id: int, direccion_id: int, direccion_data: DireccionCreate):
    direccion = db.query(Direccion).filter(
        Direccion.id == direccion_id,
        Direccion.id_usuario == user_id
    ).first()

    # Validamos que la dirección exista para el usuario
    if not direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )
        
    # Validamos que no se pueda actualizar una dirección activa
    if direccion.es_activa and not direccion_data.es_activa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes actualizar una dirección que ya está activa"
        )

    # Si se está activando esta dirección, desactivamos las otras
    if direccion_data.es_activa:
        db.query(Direccion).filter(
            Direccion.id_usuario == user_id,
            Direccion.id != direccion_id,
            Direccion.es_activa == True
        ).update({"es_activa": False})

    # Actualizamos todos los campos, incluido es_activa
    direccion.numero_calle = direccion_data.numero_calle
    direccion.region = direccion_data.region
    direccion.comuna = direccion_data.comuna
    direccion.indicaciones = direccion_data.indicaciones
    direccion.tipo_domicilio = direccion_data.tipo_domicilio
    direccion.es_activa = direccion_data.es_activa

    db.commit()
    db.refresh(direccion)

    return direccion

# Eliminar una dirección específica por ID
def delete_address_by_id(db: Session, user_id: int, direccion_id: int):
    direccion = db.query(Direccion).filter(
        Direccion.id == direccion_id,
        Direccion.id_usuario == user_id
    ).first()

    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")

    if direccion.es_activa:
        raise HTTPException(status_code=400, detail="No se puede eliminar una dirección activa")

    db.delete(direccion)
    db.commit()

    return {"message": "Dirección eliminada correctamente"}


#FUNCIONES COMPLEMENTARIAS
# Obtener todas las direcciones de un usuario
def get_all_addresses(db: Session, user_id: int):
    return db.query(Direccion).filter(Direccion.id_usuario == user_id).all()
#FUNCIONES COMPLEMENTARIAS