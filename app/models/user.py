from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String, index=True)
    birth_date = Column(String, index=True)
    is_admin = Column(Boolean, default=False)

    # Relación con direccion (bidireccional)
    address = relationship("Address", back_populates="user")
