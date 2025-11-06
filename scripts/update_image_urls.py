"""
Script para actualizar las URLs de imágenes de los productos
"""
import sys
from pathlib import Path

# Asegurar que la ruta del proyecto esté en sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.cnx import SessionLocal
from productos.model import Product
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_image_urls():
    """Actualiza todas las URLs de imágenes para usar /static/uploads/buzo.jpeg"""
    db = None
    try:
        db = SessionLocal()
        productos = db.query(Product).all()
        count = 0
        for producto in productos:
            if not producto.image_url or not producto.image_url.startswith('http'):
                producto.image_url = '/static/uploads/buzo.jpeg'
                count += 1
        
        db.commit()
        logger.info(f"✅ Se actualizaron {count} URLs de imágenes")
    except Exception as e:
        logger.error(f"❌ Error al actualizar URLs: {e}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    update_image_urls()