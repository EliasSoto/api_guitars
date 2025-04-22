from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.base import Base

class Direccion(Base):
    __tablename__ = "direccion"

    id = Column(Integer, primary_key=True, index=True)
    numero_calle = Column(String, index=True)
    region = Column(String, index=True)
    comuna = Column(String, index=True)
    indicaciones = Column(String, nullable=True)
    tipo_domicilio = Column(String, index=True)
    es_activa = Column(Boolean, default=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relación con usuario (bidireccional)
    usuario = relationship("Usuario", back_populates="direccion")
