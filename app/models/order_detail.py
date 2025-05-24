from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    guitar_id = Column(Integer, ForeignKey("guitars.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    # Relaciones
    guitar = relationship("Guitar", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")
