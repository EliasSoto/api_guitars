from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class OrderShipmentDetail(Base):
    __tablename__ = "order_shipment_details"

    tracking_number_id = Column(Integer, ForeignKey("shipments.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)

    # Relaciones
    order = relationship("Order", back_populates="shipment_details")
    shipment = relationship("Shipment", back_populates="order_details")