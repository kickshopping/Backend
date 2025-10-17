"""
Servicios para la lógica del carrito de compras.
Contienen funciones para crear productos, gestionar carritos, agregar, calcular, remover y vaciar items.
"""

from sqlalchemy.orm import Session  # Importa la sesión de SQLAlchemy
from cart.models.cart_models import Product, Cart, CartItem  # Importa los modelos
from cart.schemas.cart_schemas import ProductCreate, CartItemCreate  # Importa los schemas

def create_product(db: Session, producto: ProductCreate):
    """
    Crea un nuevo producto en la base de datos.
    """
    db_producto = Product(**producto.dict())  # Instancia el modelo con los datos recibidos
    db.add(db_producto)  # Agrega el producto a la sesión
    db.commit()  # Guarda los cambios
    db.refresh(db_producto)  # Actualiza el objeto con datos de la base
    return db_producto

def get_or_create_cart(db: Session, user_id: str):
    """
    Obtiene el carrito de un usuario o lo crea si no existe.
    """
    carrito = db.query(Cart).filter(Cart.user_id == user_id).first()  # Busca el carrito
    if not carrito:
        carrito = Cart(user_id=user_id)  # Crea uno nuevo si no existe
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    return carrito

def add_item_to_cart(db: Session, user_id: str, item: CartItemCreate):
    """
    Agrega un producto al carrito del usuario.
    Si el producto ya está, suma la cantidad; si no, lo agrega.
    """
    carrito = get_or_create_cart(db, user_id)
    producto = db.query(Product).filter(Product.id == item.product_id).first()
    if not producto:
        raise ValueError("Producto no encontrado")
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == carrito.id,
        CartItem.product_id == item.product_id
    ).first()
    if cart_item:
        cart_item.cantidad += item.cantidad  # Suma cantidad si ya existe
    else:
        cart_item = CartItem(cart_id=carrito.id, product_id=item.product_id, cantidad=item.cantidad)
        db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def calculate_cart_total(db: Session, carrito: Cart):
    """
    Calcula el total del carrito sumando precio*cantidad de cada item.
    """
    total = 0.0
    for item in carrito.items:
        total += item.cantidad * item.producto.precio
    return total

def remove_item_from_cart(db: Session, user_id: str, product_id: int):
    """
    Remueve un producto del carrito del usuario.
    """
    carrito = get_or_create_cart(db, user_id)
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == carrito.id,
        CartItem.product_id == product_id
    ).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return True
    return False

def clear_cart(db: Session, user_id: str):
    """
    Vacía todos los items del carrito del usuario.
    """
    carrito = get_or_create_cart(db, user_id)
    db.query(CartItem).filter(CartItem.cart_id == carrito.id).delete()
    db.commit()
