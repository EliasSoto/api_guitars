from sqlalchemy import Boolean, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    shipment_date = Column(Date)
    tracking_status = Column(String, index=True)
    delivery_date = Column(Date, nullable=True)
    price = Column(Float)
    shipping_provider = Column(String, index=True)
    is_immediate_delivery = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Relaciones
    user = relationship("User", back_populates="shipments")
    shipment_details = relationship("ShipmentDetail", back_populates="shipment")
