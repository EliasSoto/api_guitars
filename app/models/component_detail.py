from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class ComponentDetail(Base):
    __tablename__ = "component_details"

    guitar_detail_id = Column(Integer, ForeignKey("guitar_details.id"), primary_key=True)
    component_id = Column(Integer, ForeignKey("components.id"), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    extra_price = Column(Float, nullable=False, default=0.0)

    # Relaciones
    guitar_detail = relationship("GuitarDetail", back_populates="component_details")
    component = relationship("Component", back_populates="component_details")
