"""
Seeder para la carga inicial de productos del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlite3 import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from productos.model import Product
import logging
from datetime import date

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
    print("ℹ️ Insertando productos de calzado deportivo")
    
    try:
        # Definir productos del sistema
        productos_data = [
            {
                "name": "Nike Air Max 270",
                "description": "Zapatillas deportivas con cámara de aire visible y diseño moderno. Perfectas para uso diario y actividades deportivas.",
                "price": 129.99,
                "image_url": "https://images.nike.com/is/image/DotCom/air-max-270",
                "discount": 15.0
            },
            {
                "name": "Adidas UltraBoost 22",
                "description": "Zapatillas de running con tecnología Boost para máxima comodidad y retorno de energía.",
                "price": 180.00,
                "image_url": "https://assets.adidas.com/images/ultraboost-22",
                "discount": 0.0
            },
            {
                "name": "Puma RS-X³",
                "description": "Sneakers retro-futuristas con diseño llamativo y excelente amortiguación.",
                "price": 110.00,
                "image_url": "https://images.puma.com/image/rs-x3",
                "discount": 20.0
            },
            {
                "name": "Converse Chuck Taylor All Star",
                "description": "Zapatillas clásicas de lona, icónicas y versátiles para cualquier ocasión.",
                "price": 65.00,
                "image_url": "https://www.converse.com/chuck-taylor-all-star",
                "discount": 10.0
            },
            {
                "name": "New Balance 990v5",
                "description": "Zapatillas premium fabricadas en USA con materiales de alta calidad y comodidad superior.",
                "price": 175.00,
                "image_url": "https://nb.scene7.com/is/image/NB/990v5",
                "discount": 0.0
            },
            {
                "name": "Vans Old Skool",
                "description": "Zapatillas de skate clásicas con diseño atemporal y suela waffle distintiva.",
                "price": 60.00,
                "image_url": "https://images.vans.com/old-skool-classic",
                "discount": 25.0
            },
            {
                "name": "Jordan 1 Retro High",
                "description": "Zapatillas de baloncesto icónicas con estilo vintage y construcción premium.",
                "price": 170.00,
                "image_url": "https://static.nike.com/jordan-1-retro-high",
                "discount": 0.0
            },
            {
                "name": "Reebok Classic Leather",
                "description": "Zapatillas de cuero suave con diseño minimalista y comodidad duradera.",
                "price": 75.00,
                "image_url": "https://assets.reebok.com/classic-leather",
                "discount": 30.0
            },
            {
                "name": "ASICS Gel-Kayano 29",
                "description": "Zapatillas de running estables con tecnología GEL para máximo soporte y amortiguación.",
                "price": 160.00,
                "image_url": "https://images.asics.com/gel-kayano-29",
                "discount": 12.0
            },
            {
                "name": "Fila Disruptor II",
                "description": "Zapatillas chunky con plataforma alta y estilo retro de los 90s.",
                "price": 70.00,
                "image_url": "https://www.fila.com/disruptor-ii",
                "discount": 18.0
            },
            {
                "name": "Under Armour HOVR Phantom 3",
                "description": "Zapatillas de training con tecnología HOVR para retorno de energía y conectividad digital.",
                "price": 140.00,
                "image_url": "https://underarmour.scene7.com/hovr-phantom-3",
                "discount": 8.0
            },
            {
                "name": "Skechers D'Lites",
                "description": "Zapatillas cómodas con suela gruesa y diseño deportivo casual para uso diario.",
                "price": 85.00,
                "image_url": "https://www.skechers.com/dlites-biggest-fan",
                "discount": 22.0
            }
        ]
        
        productos_creados = 0
        
        for producto_info in productos_data:
            # Verificar si el producto ya existe (por nombre)
            existing_producto = db.query(Product).filter(
                Product.name == producto_info["name"]
            ).first()
            
            if not existing_producto:
                nuevo_producto = Product(
                    name=producto_info["name"],
                    description=producto_info["description"],
                    price=producto_info["price"],
                    image_url=producto_info["image_url"],
                    discount=producto_info["discount"]
                )
                db.add(nuevo_producto)
                productos_creados += 1
                print(f"✓ Creando producto: {producto_info['name']} - ${producto_info['price']}")
                if producto_info["discount"] > 0:
                    print(f"  🏷️ Con descuento del {producto_info['discount']}%")
                logger.info(f"🛍️ Creando producto: {producto_info['name']} - ${producto_info['price']}")
            else:
                print(f"- Producto '{producto_info['name']}' ya existe, omitiendo...")
                logger.info(f"⚠️ Producto '{producto_info['name']}' ya existe, omitiendo...")
        
        # Confirmar cambios
        db.commit()
        
        print(f"\n✅ Seeding completado exitosamente!")
        print(f"📊 Productos creados: {productos_creados}")
        print(f"🛍️ Total de productos en sistema: {db.query(Product).count()}")
        
        logger.info(f"✅ Seeding de productos completado - {productos_creados} productos creados")
        
    except IntegrityError as e:
        db.rollback()
        error_msg = f"Error de integridad en la base de datos: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        raise
        
    except Exception as e:
        db.rollback()
        error_msg = f"Error inesperado durante el seeding: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        raise
        
    finally:
        db.close()

def run_seed():
    """Ejecutar el seeding completo de productos"""
    try:
        print("🏁 Iniciando proceso de seeding de productos...")
        
        # Crear tablas si no existen
        create_products_table()
        
        # Cargar productos
        seed_productos()
        
        print("🎉 Proceso de seeding de productos completado exitosamente!")
        
    except Exception as e:
        print(f"💥 Error durante el proceso de seeding: {e}")
        logger.error(f"Error durante el proceso de seeding: {e}")
        raise

if __name__ == "__main__":
    run_seed()