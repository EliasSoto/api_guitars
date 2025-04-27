from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street_name = Column(String, index=True)
    region = Column(String, index=True)
    commune = Column(String, index=True)
    directions = Column(String, nullable=True)
    address_type = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relación con usuario (bidireccional)
    user = relationship("User", back_populates="address")
