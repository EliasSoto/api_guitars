from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import review as review_schema
from repositories import review_repo
from database.session import get_db
from core.auth import verify_token

router = APIRouter()

### ENDPOINTS PARA USUARIOS NORMALES ###

# Crear una reseña
@router.post("/usuarios/resenas", tags=["Reseñas Usuario"], response_model=review_schema.ReviewRead)
def create_review(
    review: review_schema.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden dejar reseñas"
        )

    return review_repo.create_review(db=db, user_id=current_user["id"], review=review)


# Obtener reseñas del usuario autenticado
@router.get("/usuarios/reseñas", tags=["Reseñas Usuario"], response_model=List[review_schema.ReviewRead])
def get_user_reviews(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden ver sus reseñas"
        )

    return review_repo.get_user_reviews(db=db, user_id=current_user["id"])


# Obtener una reseña propia por ID
@router.get("/usuarios/resenas/{review_id}", tags=["Reseñas Usuario"], response_model=review_schema.ReviewRead)
def get_user_review_by_id(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    return review_repo.get_review_by_id_and_user(db=db, review_id=review_id, user_id=current_user["id"])

# Obtener reseña propia por ID de guitarra
@router.get("/usuarios/guitarras/{guitar_id}/resenas", tags=["Reseñas Usuario"], response_model=review_schema.ReviewRead)
def get_my_review_by_guitar_id(
    guitar_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden ver sus reseñas"
        )
    
    review = review_repo.get_review_by_guitar_and_user(db=db, guitar_id=guitar_id, user_id=current_user["id"])
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada para esta guitarra")
    return review

# Actualizar reseña propia
@router.put("/usuarios/resenas/{review_id}", tags=["Reseñas Usuario"], response_model=review_schema.ReviewRead)
def update_user_review(
    review_id: int,
    review: review_schema.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden modificar sus reseñas"
        )

    return review_repo.update_review(db=db, review_id=review_id, user_id=current_user["id"], data=review)


# Eliminar reseña propia
@router.delete("/usuarios/resenas/{review_id}", tags=["Reseñas Usuario"])
def delete_user_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los usuarios pueden eliminar sus reseñas"
        )
    
    return review_repo.delete_review(db=db, review_id=review_id, user_id=current_user["id"])


### ENDPOINTS PÚBLICOS ###

# Obtener todas las reseñas de una guitarra
@router.get("/guitarras/{guitar_id}/resenas", tags=["Reseñas Públicas"], response_model=List[review_schema.ReviewRead])
def get_reviews_by_guitar(
    guitar_id: int,
    db: Session = Depends(get_db)
):
    return review_repo.get_reviews_by_guitar(db=db, guitar_id=guitar_id)

# Obtener promedio de reseñas de una guitarra
@router.get("/guitarras/{guitar_id}/resenas/promedio", tags=["Reseñas Públicas"], response_model=float)
def get_average_rating_by_guitar(
    guitar_id: int,
    db: Session = Depends(get_db)
):
    average_rating = review_repo.get_average_rating_by_guitar(db=db, guitar_id=guitar_id)
    return average_rating