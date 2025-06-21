from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Index
from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy.types import JSON

class Component(Base):
    __tablename__ = "component"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    subtype = Column(String, nullable=True)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    net_price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    purchase_date = Column(Date)
    brand = Column(String)
    material = Column(String)
    image_link = Column(String)
    position = Column(String)
    is_active = Column(Boolean, default=True, nullable=True)

    # Relaciones
    component_details = relationship("ComponentDetail", back_populates="component")

    # Indices compuestos
    __table_args__ = (
        Index('ix_component_type_subtype', "type", "subtype"),
        Index('ix_component_type_subtype_active_stock', "type", "subtype", "is_active", "stock"),
    )