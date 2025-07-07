from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from database.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date)
    total_price = Column(Float)
    status = Column(String, index=True)
    payment_method = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relaciones
    user = relationship("User", back_populates="orders")
    shipment_details = relationship("ShipmentDetail", back_populates="order", cascade="all, delete-orphan")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
