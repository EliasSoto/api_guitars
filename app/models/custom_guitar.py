from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from database.base import Base

class CustomGuitar(Base):
    __tablename__ = "custom_guitar"

    id = Column(Integer, primary_key=True, index=True)
    guitar_id = Column(Integer, ForeignKey("guitars.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, default=0.0)
    custom_color = Column(String(length=7), nullable=True)
    custom_fret = Column(Integer, nullable=True)
    jack_position = Column(String, nullable=True)

    # Relaciiones
    guitar = relationship("Guitar")
    component_details = relationship("ComponentDetail", back_populates="custom_guitar")
    user = relationship("User", back_populates="custom_guitars")
    order_details = relationship("OrderDetail", back_populates="custom_guitar")
