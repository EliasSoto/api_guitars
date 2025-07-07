from sqlalchemy import Column, Integer, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import relationship
from database.base import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Clave primaria artificial
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    guitar_id = Column(Integer, ForeignKey("guitars.id"), nullable=True)
    custom_guitar_id = Column(Integer, ForeignKey("custom_guitar.id", ondelete="CASCADE"), nullable=True)
    
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    # Restricción para asegurar que solo se puede tener un tipo de guitarra por orden
    __table_args__ = (
        CheckConstraint(
            '(guitar_id IS NOT NULL AND custom_guitar_id IS NULL) OR '
            '(guitar_id IS NULL AND custom_guitar_id IS NOT NULL)',
            name="check_only_one_guitar_type"
        ),
    )

    guitar = relationship("Guitar", back_populates="order_details")
    custom_guitar = relationship("CustomGuitar", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")
