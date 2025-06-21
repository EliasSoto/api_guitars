from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.base import Base

class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    guitar_id = Column(Integer, ForeignKey("guitars.id", ondelete="CASCADE"))

    # Para que un usuario no pueda agregar la misma guitarra más de una vez
    __table_args__ = (UniqueConstraint("user_id", "guitar_id", name="unique_wishlist"),)

    # Relaciones
    user = relationship("User", back_populates="wishlists")
    guitar = relationship("Guitar", back_populates="wishlists")
