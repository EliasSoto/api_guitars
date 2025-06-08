from sqlalchemy import Boolean, Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from database.base import Base

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    iva = Column(Float)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    net_price = Column(Float)
    liquidation_price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    purchase_date = Column(Date)
    brand = Column(String)
    material = Column(String)
    position = Column(String)
    is_active = Column(Boolean, default=True)

    # Relación con ComponentDetail
    component_details = relationship("ComponentDetail", back_populates="component")
