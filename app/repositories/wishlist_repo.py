from sqlalchemy.orm import Session
from app.models.wishlist import Wishlist
from app.models.user import User
from app.models.guitar import Guitar
from fastapi import HTTPException, status
from app.schemas import wishlist as wishlist_schema
from app.schemas.wishlist import WishlistListResponse

### FUNCIONES USUARIO ###

# Crear un item en wishlist
def create_wishlist_item(db: Session, user_id: int, guitar_id: int):
    # Verificamos si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificamos si la guitarra existe
    guitar = db.query(Guitar).filter(Guitar.id == guitar_id).first()
    if not guitar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guitarra no encontrada"
        )
    
    # Verificamos si ya existe en wishlist
    existing_item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.guitar_id == guitar_id
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este producto ya está en tu wishlist."
        )
    
    db_item = Wishlist(user_id=user_id, guitar_id=guitar_id)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Obtener wishlist de un usuario (paginados)
def get_wishlist_by_user(db: Session, user_id: int, page: int, limit: int):
    offset = (page - 1) * limit

    wishlist = (
        db.query(Wishlist)
        .filter(Wishlist.user_id == user_id)
        .order_by(Wishlist.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    total_items = db.query(Wishlist).filter(Wishlist.user_id == user_id).count()

    if not wishlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron guitarras de la lista de deseados en esta página."
        )
    
    return WishlistListResponse(wishlist=wishlist, total=total_items)

# Eliminar un item de wishlist por id
def delete_wishlist_item(db: Session, wishlist_id: int, user_id: int):
    db_item = db.query(Wishlist).filter(
        Wishlist.id == wishlist_id,
        Wishlist.user_id == user_id
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la guitarra en la lista de deseados para eliminar"
        )
    
    db.delete(db_item)
    db.commit()
    return db_item

# Eliminar un item por id de guitarra
def delete_wishlist_item_by_guitar(db: Session, user_id: int, guitar_id: int):
    db_item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.guitar_id == guitar_id
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la guitarra en la lista de deseados para eliminar"
        )
    
    db.delete(db_item)
    db.commit()
    return db_item

# Obtener un item por id de guitarra
def get_wishlist_item_by_user_and_guitar(db: Session, user_id: int, guitar_id: int):
    db_item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.guitar_id == guitar_id
    ).first()
    
    return db_item
