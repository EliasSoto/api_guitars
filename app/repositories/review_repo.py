from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.review import Review
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.schemas import review as review_schema

# Obtener IDs de guitarras que el usuario ha comprado
def get_user_ordered_guitar_ids(db: Session, user_id: int) -> list[int]:
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    if not orders:
        return []

    order_ids = [order.id for order in orders]
    order_details = db.query(OrderDetail).filter(OrderDetail.order_id.in_(order_ids)).all()
    guitar_ids = list({detail.guitar_id for detail in order_details})
    return guitar_ids

# Crear una reseña
def create_review(db: Session, user_id: int, review: review_schema.ReviewCreate):
    try:
        # Validar si ya existe una reseña del usuario para la misma guitarra
        existing_review = db.query(Review).filter(
            Review.user_id == user_id,
            Review.guitar_id == review.guitar_id
        ).first()

        if existing_review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya has dejado una reseña para esta guitarra."
            )

        # Validar si el usuario ha comprado la guitarra
        ordered_guitar_ids = get_user_ordered_guitar_ids(db, user_id)
        if review.guitar_id not in ordered_guitar_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes dejar reseñas de guitarras que hayas comprado."
            )

        # Crear la reseña
        db_review = Review(
            user_id=user_id,
            guitar_id=review.guitar_id,
            rating=review.rating,
            comment=review.comment
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la reseña: {str(e)}"
        )

# Obtener todas las reseñas de una guitarra
def get_reviews_by_guitar(db: Session, guitar_id: int):
    reviews = db.query(Review).filter(Review.guitar_id == guitar_id).all()
    return reviews

# Obtener una reseña por ID y usuario (solo puede ver la suya)
def get_review_by_id_and_user(db: Session, review_id: int, user_id: int):
    review = db.query(Review).filter_by(id=review_id, user_id=user_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada"
        )
    return review

# Obtener todas las reseñas de un usuario
def get_user_reviews(db: Session, user_id: int):
    return db.query(Review).filter(Review.user_id == user_id).all()

# Actualizar una reseña
def update_review(db: Session, review_id: int, user_id: int, data: review_schema.ReviewUpdate):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada"
        )

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)
    return review

# Eliminar una reseña
def delete_review(db: Session, review_id: int, user_id: int):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada"
        )

    db.delete(review)
    db.commit()
    return {"message": "Reseña eliminada exitosamente"}

# Obtener el promedio de las reseñas de una guitarra
def get_average_rating_by_guitar(db: Session, guitar_id: int):
    average_rating = db.query(Review.rating).filter(Review.guitar_id == guitar_id).all()
    if not average_rating:
        return 0.0

    total_rating = sum(rating[0] for rating in average_rating)
    count = len(average_rating)
    return round(total_rating / count, 2) if count > 0 else 0.0