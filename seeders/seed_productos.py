
"""
Seeder de productos de ropa para hombre, mujer y unisex, organizado por secciones.
"""
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from productos.model import Product
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_products_table():
    """Crear las tablas de productos si no existen"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas de productos creadas/verificadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise

def seed_productos():
    """Cargar productos básicos en la base de datos"""
    db = SessionLocal()
    
    print("=== Iniciando carga de productos ===")
    
    productos = [
        # Hombre
        {"name": "Calzón Calvin Klein", "description": "Calzón cómodo para hombre", "price": 3500, "image_url": "/buzo.jpeg", "discount": 5},
        {"name": "Gorra Nike", "description": "Gorra deportiva para hombre", "price": 4000, "image_url": "/buzo.jpeg", "discount": 10},
        {"name": "Campera North Face", "description": "Campera impermeable para hombre", "price": 25000, "image_url": "/buzo.jpeg", "discount": 15},
        {"name": "Buzo Adidas", "description": "Buzo de algodón para hombre", "price": 12000, "image_url": "/buzo.jpeg", "discount": 10},
        {"name": "Pantalón Levis", "description": "Pantalón de jean para hombre", "price": 11000, "image_url": "/buzo.jpeg", "discount": 10},
        {"name": "Remera Nike", "description": "Remera deportiva para hombre", "price": 8000, "image_url": "/buzo.jpeg", "discount": 5},
        {"name": "Camisa Zara", "description": "Camisa casual para hombre", "price": 9500, "image_url": "/buzo.jpeg", "discount": 0},
        {"name": "Zapatillas Puma", "description": "Zapatillas deportivas para hombre", "price": 18000, "image_url": "/buzo.jpeg", "discount": 20},

        # Mujer
        {"name": "Vestido Mango", "description": "Vestido elegante para mujer", "price": 15000, "image_url": "/buzo.jpeg", "discount": 15},
        {"name": "Blusa Bershka", "description": "Blusa de verano para mujer", "price": 6500, "image_url": "/buzo.jpeg", "discount": 5},
        {"name": "Falda H&M", "description": "Falda corta para mujer", "price": 7000, "image_url": "/buzo.jpeg", "discount": 0},
        {"name": "Pantalón Stradivarius", "description": "Pantalón de vestir para mujer", "price": 10500, "image_url": "/buzo.jpeg", "discount": 8},
        {"name": "Remera Zara Mujer", "description": "Remera básica para mujer", "price": 7500, "image_url": "/buzo.jpeg", "discount": 5},
        {"name": "Zapatillas Adidas Mujer", "description": "Zapatillas deportivas para mujer", "price": 17500, "image_url": "/buzo.jpeg", "discount": 18},
        {"name": "Bolso Tous", "description": "Bolso elegante para mujer", "price": 22000, "image_url": "/buzo.jpeg", "discount": 12},
        {"name": "Accesorio Pandora", "description": "Pulsera de plata para mujer", "price": 9000, "image_url": "/buzo.jpeg", "discount": 10},

        # Unisex
        {"name": "Pantalón Levis Unisex", "description": "Pantalón de jean unisex", "price": 11000, "image_url": "/buzo.jpeg", "discount": 10},
        {"name": "Remera Unisex", "description": "Remera básica unisex", "price": 7000, "image_url": "/buzo.jpeg", "discount": 5},
        {"name": "Zapatillas Puma Unisex", "description": "Zapatillas deportivas unisex", "price": 18000, "image_url": "/buzo.jpeg", "discount": 20},
        {"name": "Bolso Unisex", "description": "Bolso casual unisex", "price": 15000, "image_url": "/buzo.jpeg", "discount": 10},
        {"name": "Accesorio Unisex", "description": "Collar de acero unisex", "price": 6000, "image_url": "/buzo.jpeg", "discount": 8},
    ]
    
    try:
        productos_creados = 0
        
        for producto_info in productos:
            # Verificar si el producto ya existe
            existing_producto = db.query(Product).filter(Product.name == producto_info["name"]).first()
            
            if not existing_producto:
                nuevo_producto = Product(**producto_info)
                db.add(nuevo_producto)
                productos_creados += 1
                print(f"✓ Creando producto: {producto_info['name']}")
                logger.info(f"📦 Creando producto: {producto_info['name']}")
            else:
                print(f"- Producto '{producto_info['name']}' ya existe, omitiendo...")
                logger.info(f"⚠️  Producto '{producto_info['name']}' ya existe, omitiendo...")
        
        db.commit()
        
        if productos_creados > 0:
            print(f"✓ Se crearon {productos_creados} productos exitosamente")
            logger.info(f"✅ Se crearon {productos_creados} productos exitosamente")
        else:
            print("ℹ️ Todos los productos ya existían")
            logger.info("ℹ️  Todos los productos ya existían")
            
    except Exception as e:
        db.rollback()
        print(f"✗ Error inesperado al crear productos: {e}")
        logger.error(f"❌ Error inesperado al crear productos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Productos ===")
    create_products_table()
    seed_productos()
    print("=== Finalizado ===")