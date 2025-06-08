from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class GuitarDetail(Base):
    __tablename__ = "guitar_details"

    id = Column(Integer, primary_key=True, index=True)
    customization_price = Column(Float, nullable=False)
    work_price = Column(Float, nullable=False)
    guitar_id = Column(Integer, ForeignKey("guitars.id"), nullable=False)

    # Relaciones
    guitar = relationship("Guitar", back_populates="guitar_details")
    component_details = relationship("ComponentDetail", back_populates="guitar_detail")
