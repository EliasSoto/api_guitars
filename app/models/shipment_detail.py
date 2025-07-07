from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class ShipmentDetail(Base):
    __tablename__ = "shipment_details"

    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True) 

    # Relaciones
    order = relationship("Order", back_populates="shipment_details")
    shipment = relationship("Shipment", back_populates="shipment_details")

    