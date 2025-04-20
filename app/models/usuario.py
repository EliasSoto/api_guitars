from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String, index=True)
    nombres = Column(String, unique=True, index=True)
    apellidos = Column(String, index=True)
    correo = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    telefono = Column(String, index=True)
    fecha_nacimiento = Column(String, index=True)
    es_administrador = Column(Boolean, default=False)

    # Relación con direccion (bidireccional)
    direccion = relationship("Direccion", back_populates="usuario")
