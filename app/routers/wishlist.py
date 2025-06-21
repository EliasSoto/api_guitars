from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas import wishlist as wishlist_schema
from app.repositories import wishlist_repo
from database.session import get_db
from core.auth import verify_token

router = APIRouter()

### ENDPOINTS DE WISHLIST ###

# Obtener lista de wishlist de un usuario logueado
@router.get("/wishlist", tags=["Wishlist"], response_model=wishlist_schema.WishlistListResponse)
def get_my_wishlist(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver la lista de deseados"
        )
        
    return wishlist_repo.get_wishlist_by_user(db=db, user_id=current_user["id"], page=page, limit=limit)


# Agregar una guitarra a la wishlist
@router.post("/wishlist/{guitar_id}", tags=["Wishlist"], response_model=wishlist_schema.WishlistRead)
def add_to_wishlist(
    guitar_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para añadir a la lista de deseados"
        )
        
    return wishlist_repo.create_wishlist_item(db=db, user_id=current_user["id"], guitar_id=guitar_id)


# Eliminar una guitarra de la wishlist
@router.delete("/wishlist/{guitar_id}", tags=["Wishlist"])
def delete_from_wishlist(
    guitar_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar de la lista de deseados"
        )
        
    wishlist_repo.delete_wishlist_item_by_guitar(db=db, user_id=current_user["id"], guitar_id=guitar_id)
    return {"message": "Item de wishlist eliminado correctamente"}


# Saber si una guitarra está en la wishlist
@router.get("/wishlist/check/{guitar_id}", tags=["Wishlist"])
def is_in_wishlist(
    guitar_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver si guitarra está en la lista de deseados"
        )
        
    item = wishlist_repo.get_wishlist_item_by_user_and_guitar(db=db, user_id=current_user["id"], guitar_id=guitar_id)
    return {"is_in_wishlist": bool(item)}
