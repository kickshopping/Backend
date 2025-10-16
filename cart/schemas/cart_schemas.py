"""
Schemas Pydantic para la validación y serialización de datos de productos, items y carritos.
Permiten definir la estructura esperada en las peticiones y respuestas de la API.
"""

from pydantic import BaseModel  # Importa la clase base de Pydantic
from typing import Optional, List  # Importa tipos para campos opcionales y listas

class ProductCreate(BaseModel):
    """
    Schema para crear un producto.
    Define los campos requeridos y opcionales.
    """
    nombre: str  # Nombre del producto
    descripcion: Optional[str] = None  # Descripción opcional
    precio: float  # Precio del producto

class ProductOut(BaseModel):
    """
    Schema para mostrar un producto en respuestas.
    Incluye el id y todos los campos relevantes.
    """
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float

    class Config:
        orm_mode = True  # Permite compatibilidad con modelos ORM

class CartItemCreate(BaseModel):
    """
    Schema para agregar un producto al carrito.
    """
    product_id: int  # ID del producto a agregar
    cantidad: int = 1  # Cantidad (por defecto 1)

class CartItemOut(BaseModel):
    """
    Schema para mostrar un item del carrito en respuestas.
    """
    id: int
    product_id: int
    cantidad: int
    producto: ProductOut  # Datos completos del producto

    class Config:
        orm_mode = True

class CartOut(BaseModel):
    """
    Schema para mostrar el carrito completo y el total.
    """
    id: int
    user_id: str
    items: List[CartItemOut]  # Lista de items en el carrito
    total: float  # Total calculado

    class Config:
        orm_mode = True
