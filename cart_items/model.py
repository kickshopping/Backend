from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.basemodel import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.usu_id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    
    # Relaciones
    user = relationship("Usuario", lazy="joined")
    product = relationship("Product", back_populates="cart_items", lazy="joined")