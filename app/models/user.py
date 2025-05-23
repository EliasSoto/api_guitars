from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.base import Base
from .order import Order
from .shipment import Shipment
from .order_detail import OrderDetail
from .shipment_detail import ShipmentDetail

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)
    birth_date = Column(String)
    is_admin = Column(Boolean, default=False)

    # Relaciones
    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")
