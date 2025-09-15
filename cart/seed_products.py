# cart/seed_products.py
"""
Script para insertar productos de prueba en la base de datos.
Permite poblar la tabla de productos con ejemplos iniciales.
"""

from config.cnx import SessionLocal  # Importa la sesión de base de datos
from cart.models.cart_models import Product  # Importa el modelo de producto

def insertar_productos():
    """
    Inserta una lista de productos de ejemplo si no existen en la base de datos.
    """
    productos = [
        {"nombre": "Zapatillas Nike Air", "descripcion": "Zapatillas deportivas", "precio": 120.0},
        {"nombre": "Camiseta Adidas", "descripcion": "Camiseta de algodón", "precio": 35.0},
        {"nombre": "Gorra Puma", "descripcion": "Gorra ajustable", "precio": 20.0},
        {"nombre": "Sudadera Reebok", "descripcion": "Sudadera con capucha", "precio": 50.0}
    ]
    db = SessionLocal()  # Crea una sesión de base de datos
    for prod in productos:
        existe = db.query(Product).filter(Product.nombre == prod["nombre"]).first()  # Verifica si ya existe
        if not existe:
            producto = Product(**prod)  # Instancia el producto
            db.add(producto)  # Lo agrega a la sesión
    db.commit()  # Guarda los cambios
    db.close()  # Cierra la sesión
    print("Productos de prueba insertados correctamente.")

if __name__ == "__main__":
    insertar_productos()  # Ejecuta la función si el script se corre directamente
