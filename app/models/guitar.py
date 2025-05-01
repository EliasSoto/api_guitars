from sqlalchemy import Boolean, Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from database.base import Base

class Guitar(Base):
    __tablename__ = "guitars"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    purchase_price = Column(Float)
    sale_price = Column(Float)
    net_price = Column(Float)
    iva = Column(Float)
    liquidation_price = Column(Float)
    purchase_date = Column(Date)
    wood_type = Column(String)
    image_link = Column(String)
    color = Column(String)
    stock = Column(Integer)
    is_custom = Column(Boolean, default=False)
    fret_count = Column(Integer)
    
    # Relaciones
    order_details = relationship("OrderDetail", back_populates="guitar")
