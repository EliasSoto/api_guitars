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
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Relaciones
    user = relationship("User", back_populates="orders")
    shipment_details = relationship("OrderShipmentDetail", back_populates="order")
    order_details = relationship("OrderDetail", back_populates="order")
