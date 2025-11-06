from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config.basemodel import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    image_url = Column(String, nullable=True)
    discount = Column(Float, default=0.0)
    category = Column(String, nullable=True, index=True)  # Nueva columna para categorías

    # Relación con items del carrito
    cart_items = relationship("CartItem", back_populates="product")

