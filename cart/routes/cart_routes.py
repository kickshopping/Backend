"""
Rutas de FastAPI para la gestión del carrito de compras.
Define los endpoints para crear productos, agregar al carrito, ver el carrito, remover y vaciar.
"""

from fastapi import APIRouter, Depends, HTTPException  # Importa utilidades de FastAPI
from sqlalchemy.orm import Session  # Importa la sesión de SQLAlchemy
from cart.schemas.cart_schemas import ProductCreate, ProductOut, CartItemCreate, CartOut  # Schemas Pydantic
from cart.services.cart_services import (
    create_product, get_or_create_cart, add_item_to_cart,
    calculate_cart_total, remove_item_from_cart, clear_cart
)  # Funciones de servicio
from config.cnx import SessionLocal  # Sesión de base de datos

router = APIRouter()  # Instancia el router para agrupar rutas

def get_db():
    """
    Provee una sesión de base de datos para cada request.
    Cierra la sesión al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products", response_model=ProductOut)
def crear_producto(producto: ProductCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un nuevo producto.
    Recibe los datos del producto y lo guarda en la base de datos.
    """
    return create_product(db, producto)

@router.post("/{user_id}/add")
def agregar_producto(user_id: str, item: CartItemCreate, db: Session = Depends(get_db)):
    """
    Endpoint para agregar un producto al carrito de un usuario.
    Si el producto no existe, retorna error 404.
    """
    try:
        cart_item = add_item_to_cart(db, user_id, item)
        return {"mensaje": "Producto agregado al carrito", "item_id": cart_item.id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{user_id}", response_model=CartOut)
def ver_carrito(user_id: str, db: Session = Depends(get_db)):
    """
    Endpoint para ver el carrito de un usuario y el total calculado.
    """
    carrito = get_or_create_cart(db, user_id)
    total = calculate_cart_total(db, carrito)
    return {
        "id": carrito.id,
        "user_id": carrito.user_id,
        "items": carrito.items,
        "total": total
    }

@router.delete("/{user_id}/remove/{product_id}")
def remover_producto(user_id: str, product_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para remover un producto del carrito.
    Si el producto no está en el carrito, retorna error 404.
    """
    eliminado = remove_item_from_cart(db, user_id, product_id)
    if eliminado:
        return {"mensaje": "Producto removido del carrito"}
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

@router.delete("/{user_id}/clear")
def vaciar_carrito(user_id: str, db: Session = Depends(get_db)):
    """
    Endpoint para vaciar el carrito de un usuario.
    """
    clear_cart(db, user_id)
    return {"mensaje": "Carrito vaciado"}
