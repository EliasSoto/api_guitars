from sqlalchemy.orm import Session
from models.address import Address
from app.schemas import address as address_schema
from fastapi import HTTPException, status

### FUNCIONES PARA DIRECCIONES ###

# Función para crear una nueva dirección para un usuario.
def create_address(db: Session, user_id: int, address: address_schema.AddressCreate):
    # Siempre que se crea una nueva dirección, se inactivan las anteriores.
    try:
        db.query(Address).filter(
            Address.user_id == user_id,
            Address.is_active == True  # Solo se desactivan las activas
        ).update({"is_active": False})
        
        # Se crea una nueva dirección forzadamente activa
        db_address = Address(
            street_name=address.street_name,
            region=address.region,
            commune=address.commune,
            directions=address.directions,
            address_type=address.address_type,
            user_id=user_id,
            is_active=True
        )

        db.add(db_address)
        db.commit()
        db.refresh(db_address)

        return db_address
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la dirección: {str(e)}"
        )

# Función para actualizar una dirección específica por id.
def update_address(db: Session, user_id: int, address_id: int, address_data: address_schema.AddressUpdate):
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    # Se verifica que la dirección exista.
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )
        
    # Se valida que no se pueda actualizar una dirección activa.
    if address.is_active and not address_data.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes actualizar una dirección que ya está activa"
        )

    # Si la nueva dirección es activa, inactivamos las anteriores.
    if address_data.is_active:
        db.query(Address).filter(
            Address.user_id == user_id,
            Address.id != address_id,
            Address.is_active == True
        ).update({"is_active": False})

    # Se actualizan los campos de la dirección.
    address.street_name = address_data.street_name
    address.region = address_data.region
    address.commune = address_data.commune
    address.directions = address_data.directions
    address.address_type = address_data.address_type
    address.is_active = address_data.is_active
        
    db.commit()
    db.refresh(address)

    return address

# Función para eliminar una dirección específica por id.
def delete_address_by_id(db: Session, user_id: int, address_id: int):
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == user_id
    ).first()

    # Se verifica que la dirección exista.
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dirección no encontrada"
        )

    # Se valida que no se pueda eliminar una dirección activa.
    if address.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una dirección activa."
        )

    db.delete(address)
    db.commit()

    return {"message": "Dirección eliminada correctamente"}

# Función para obtener todas las direcciones por id.
def get_all_addresses(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()

# Función para saber si una dirección es activa.
def get_active_address(db: Session, user_id: int):
    active_address = db.query(Address).filter(
        Address.user_id == user_id,
        Address.is_active == True
    ).first()

    return active_address

# Función para obtener todas las direcciones por id de usuario.
def get_all_addresses_by_user_id(db: Session, user_id: int):
    addresses = db.query(Address).filter(Address.user_id == user_id).all()

    if not addresses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron direcciones para este usuario"
        )

    return addresses