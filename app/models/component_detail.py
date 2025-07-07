from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.base import Base

class ComponentDetail(Base):
    __tablename__ = "component_detail"

    component_id = Column(Integer, ForeignKey("component.id"), primary_key=True)
    custom_guitar_id = Column(Integer, ForeignKey("custom_guitar.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False, default=0.0)

    # Relaciones
    component = relationship("Component", back_populates="component_details")
    custom_guitar = relationship("CustomGuitar", back_populates="component_details")
