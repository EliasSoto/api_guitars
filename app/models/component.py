from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import relationship
from database.base import Base

class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    net_price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    purchase_date = Column(Date)
    brand = Column(String)  # 'merca'
    material = Column(String)
    position = Column(String)
    is_active = Column(Boolean, default=True)

    # Relaciones
    component_details = relationship("ComponentDetail", back_populates="component")
