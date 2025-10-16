"""
Modelos SQLAlchemy para la gestión de productos, carritos y items en KickShopping.
Cada clase representa una tabla en la base de datos y define sus relaciones.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey  # Importa tipos y claves foráneas
from sqlalchemy.orm import relationship  # Importa para definir relaciones entre tablas
from config.basemodel import Base  # Importa la base declarativa

class Product(Base):
    """
    Modelo de la tabla 'products'.
    Representa un producto disponible en la tienda.
    """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)  # ID único del producto
    nombre = Column(String, unique=True, index=True, nullable=False)  # Nombre único
    descripcion = Column(String, nullable=True)  # Descripción opcional
    precio = Column(Float, nullable=False)  # Precio del producto

    items = relationship("CartItem", back_populates="producto")  # Relación con los items en carritos

class Cart(Base):
    """
    Modelo de la tabla 'carts'.
    Representa el carrito de un usuario.
    """
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)  # ID único del carrito
    user_id = Column(String, unique=True, index=True, nullable=False)  # ID del usuario (puede ser email, username, etc)

    items = relationship("CartItem", back_populates="carrito", cascade="all, delete-orphan")  # Relación con los items del carrito

class CartItem(Base):
    """
    Modelo de la tabla 'cart_items'.
    Representa un producto agregado a un carrito.
    """
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)  # ID único del item
    cart_id = Column(Integer, ForeignKey("carts.id"))  # Referencia al carrito
    product_id = Column(Integer, ForeignKey("products.id"))  # Referencia al producto
    cantidad = Column(Integer, default=1)  # Cantidad de ese producto en el carrito

    carrito = relationship("Cart", back_populates="items")  # Relación inversa con carrito
    producto = relationship("Product", back_populates="items")  # Relación inversa con producto
