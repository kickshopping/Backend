
"""
Seeder de productos de ropa para hombre, mujer y unisex, organizado por secciones.
"""
import os
import sys
from pathlib import Path

# Asegurar que la ruta del proyecto esté en sys.path cuando se ejecuta el seeder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

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
        # Calzones
                # Mujer
        # Calzones
        {"name": "Calzón Victoria's Secret", "description": "Calzón de encaje elegante", "price": 4500, "image_url": "/ropa-interior-mujer.jpeg", "discount": 20, "category": "calzones"},
        {"name": "Calzón Calvin Klein Mujer", "description": "Calzón de algodón suave", "price": 3800, "image_url": "/ropa-interior-mujer.jpeg", "discount": 0, "category": "calzones"},
        {"name": "Calzón La Perla", "description": "Calzón de lujo italiano", "price": 6000, "image_url": "/ropa-interior-mujer.jpeg", "discount": 10, "category": "calzones"},
        {"name": "Calzón Tommy Hilfiger Mujer", "description": "Calzón deportivo cómodo", "price": 3500, "image_url": "/ropa-interior-mujer.jpeg", "discount": 5, "category": "calzones"},
        {"name": "Calzón Under Armour Mujer", "description": "Calzón sin costuras", "price": 4000, "image_url": "/ropa-interior-mujer.jpeg", "discount": 15, "category": "calzones"},

        # Remeras Hombre
        {"name": "Remera Nike Dri-Fit", "description": "Remera deportiva con tecnología antisudor", "price": 8500, "image_url": "/remera-hombre.jpeg", "discount": 0, "category": "remeras-hombre"},
        {"name": "Remera Adidas Training", "description": "Remera para entrenamiento de alto rendimiento", "price": 7800, "image_url": "/remera-hombre.jpeg", "discount": 15, "category": "remeras-hombre"},
        {"name": "Remera Under Armour Tech", "description": "Remera técnica de manga corta", "price": 9000, "image_url": "/remera-hombre.jpeg", "discount": 10, "category": "remeras-hombre"},
        {"name": "Remera Puma Sport", "description": "Remera deportiva transpirable", "price": 7500, "image_url": "/remera-hombre.jpeg", "discount": 5, "category": "remeras-hombre"},
        {"name": "Remera Reebok Classic", "description": "Remera clásica de algodón", "price": 6500, "image_url": "/remera-hombre.jpeg", "discount": 0, "category": "remeras-hombre"},
        {"name": "Remera New Balance Running", "description": "Remera para corredores", "price": 8200, "image_url": "/remera-hombre.jpeg", "discount": 12, "category": "remeras-hombre"},
        
        {"name": "Campera North Face", "description": "Campera impermeable para hombre", "price": 25000, "image_url": "https://placehold.co/400x300/darkblue/white?text=North+Face", "discount": 15, "category": "camperas"},
        {"name": "Campera Columbia", "description": "Campera térmica de invierno", "price": 28000, "image_url": "https://placehold.co/400x300/darkblue/white?text=Columbia", "discount": 10, "category": "camperas"},
        {"name": "Campera Patagonia", "description": "Campera cortavientos ligera", "price": 22000, "image_url": "https://placehold.co/400x300/darkblue/white?text=Patagonia", "discount": 0, "category": "camperas"},
        
        {"name": "Buzo Adidas", "description": "Buzo de algodón para hombre", "price": 12000, "image_url": "https://placehold.co/400x300/gray/white?text=Adidas+Buzo", "discount": 10, "category": "buzos"},
        {"name": "Buzo Nike Tech", "description": "Buzo deportivo tecnológico", "price": 15000, "image_url": "https://placehold.co/400x300/gray/white?text=Nike+Tech", "discount": 5, "category": "buzos"},
        {"name": "Buzo Puma", "description": "Buzo con capucha moderno", "price": 11000, "image_url": "https://placehold.co/400x300/gray/white?text=Puma+Buzo", "discount": 15, "category": "buzos"},
        
        {"name": "Pantalón Levis", "description": "Pantalón de jean para hombre", "price": 11000, "image_url": "https://placehold.co/400x300/blue/white?text=Levis+Jean", "discount": 10, "category": "pantalones"},
        {"name": "Pantalón Cargo", "description": "Pantalón cargo militar", "price": 13000, "image_url": "https://placehold.co/400x300/darkgreen/white?text=Cargo", "discount": 0, "category": "pantalones"},
        {"name": "Pantalón Chino", "description": "Pantalón chino elegante", "price": 12500, "image_url": "https://placehold.co/400x300/khaki/black?text=Chino", "discount": 8, "category": "pantalones"},
        
        {"name": "Remera Nike", "description": "Remera deportiva para hombre", "price": 8000, "image_url": "/buzo.jpeg", "discount": 5, "category": "remeras"},
        {"name": "Remera Under Armour", "description": "Remera deportiva de compresión", "price": 9500, "image_url": "/buzo.jpeg", "discount": 0, "category": "remeras"},
        {"name": "Remera Adidas", "description": "Remera clásica de algodón", "price": 7500, "image_url": "/buzo.jpeg", "discount": 12, "category": "remeras"},
        
        {"name": "Camisa Zara", "description": "Camisa casual para hombre", "price": 9500, "image_url": "/buzo.jpeg", "discount": 0, "category": "camisas"},
        {"name": "Camisa Ralph Lauren", "description": "Camisa de vestir elegante", "price": 18000, "image_url": "/buzo.jpeg", "discount": 15, "category": "camisas"},
        {"name": "Camisa Tommy", "description": "Camisa oxford clásica", "price": 14500, "image_url": "/buzo.jpeg", "discount": 10, "category": "camisas"},
        
        # Mujer
        # Vestidos
        {"name": "Vestido Mango", "description": "Vestido elegante para mujer", "price": 15000, "image_url": "https://placehold.co/400x300/pink/white?text=Mango+Dress", "discount": 15, "category": "vestidos"},
        {"name": "Vestido Zara", "description": "Vestido casual de verano", "price": 12000, "image_url": "https://placehold.co/400x300/pink/white?text=Zara+Dress", "discount": 0, "category": "vestidos"},
        {"name": "Vestido H&M", "description": "Vestido de fiesta", "price": 18000, "image_url": "https://placehold.co/400x300/purple/white?text=H%26M+Party", "discount": 20, "category": "vestidos"},
        {"name": "Vestido Forever 21", "description": "Vestido juvenil moderno", "price": 13500, "image_url": "https://placehold.co/400x300/pink/white?text=F21+Dress", "discount": 10, "category": "vestidos"},
        {"name": "Vestido Pull&Bear", "description": "Vestido casual diario", "price": 11000, "image_url": "https://placehold.co/400x300/pink/white?text=Pull%26Bear", "discount": 5, "category": "vestidos"},
        {"name": "Vestido Bershka", "description": "Vestido corto de temporada", "price": 14000, "image_url": "https://placehold.co/400x300/pink/white?text=Bershka+Dress", "discount": 15, "category": "vestidos"},

        # Remeras Mujer
        {"name": "Remera Nike Women", "description": "Remera deportiva femenina", "price": 7500, "image_url": "https://placehold.co/400x300/pink/white?text=Nike+Women", "discount": 0, "category": "remeras-mujer"},
        {"name": "Remera Adidas Workout", "description": "Remera para ejercicio mujer", "price": 8000, "image_url": "https://placehold.co/400x300/pink/white?text=Adidas+Workout", "discount": 10, "category": "remeras-mujer"},
        {"name": "Remera Puma Fitness", "description": "Remera deportiva ajustada", "price": 7200, "image_url": "https://placehold.co/400x300/pink/white?text=Puma+Fitness", "discount": 15, "category": "remeras-mujer"},
        {"name": "Remera Under Armour Fit", "description": "Remera técnica deportiva", "price": 8500, "image_url": "https://placehold.co/400x300/pink/white?text=UA+Fit", "discount": 5, "category": "remeras-mujer"},
        {"name": "Remera Reebok Training", "description": "Remera para entrenamiento", "price": 7800, "image_url": "https://placehold.co/400x300/pink/white?text=Reebok+Training", "discount": 12, "category": "remeras-mujer"},
        {"name": "Remera Fila Sport", "description": "Remera deportiva transpirable", "price": 6800, "image_url": "https://placehold.co/400x300/pink/white?text=Fila+Sport", "discount": 8, "category": "remeras-mujer"},
        
        # Accesorios Hombre
        {"name": "Lentes de Sol Ray-Ban Aviator", "description": "Lentes de sol clásicos para hombre", "price": 45000, "image_url": "https://placehold.co/400x300/gold/black?text=RayBan+Aviator", "discount": 10, "category": "accesorios-hombre"},
        {"name": "Lentes de Sol Oakley", "description": "Lentes deportivos para hombre", "price": 52000, "image_url": "https://placehold.co/400x300/black/white?text=Oakley", "discount": 15, "category": "accesorios-hombre"},
        {"name": "Lentes de Sol Police", "description": "Lentes de sol elegantes para hombre", "price": 48000, "image_url": "https://placehold.co/400x300/silver/black?text=Police", "discount": 5, "category": "accesorios-hombre"},
        {"name": "Gorra Nike Sport", "description": "Gorra deportiva para hombre", "price": 4000, "image_url": "https://placehold.co/400x300/black/white?text=Nike+Cap", "discount": 10, "category": "accesorios-hombre"},
        {"name": "Gorra Adidas Original", "description": "Gorra clásica ajustable", "price": 3800, "image_url": "https://placehold.co/400x300/black/white?text=Adidas+Cap", "discount": 0, "category": "accesorios-hombre"},
        {"name": "Gorra New Era Premium", "description": "Gorra plana de colección", "price": 4500, "image_url": "https://placehold.co/400x300/navy/white?text=New+Era", "discount": 5, "category": "accesorios-hombre"},
        {"name": "Reloj Casio G-Shock", "description": "Reloj deportivo resistente", "price": 35000, "image_url": "https://placehold.co/400x300/black/white?text=G-Shock", "discount": 15, "category": "accesorios-hombre"},
        {"name": "Cinturón de Cuero", "description": "Cinturón de cuero genuino", "price": 12000, "image_url": "/accesorios-hombre.jpeg", "discount": 5, "category": "accesorios-hombre"},
        {"name": "Billetera Tommy Hilfiger", "description": "Billetera de cuero premium", "price": 18000, "image_url": "/accesorios-hombre.jpeg", "discount": 0, "category": "accesorios-hombre"},
        
        # Accesorios Mujer
        {"name": "Lentes de Sol Prada", "description": "Lentes de sol elegantes para mujer", "price": 52000, "image_url": "https://placehold.co/400x300/black/gold?text=Prada", "discount": 10, "category": "accesorios-mujer"},
        {"name": "Lentes de Sol Gucci", "description": "Lentes de sol de diseñador para mujer", "price": 58000, "image_url": "https://placehold.co/400x300/green/red?text=Gucci", "discount": 5, "category": "accesorios-mujer"},
        {"name": "Lentes de Sol Versace", "description": "Lentes de sol premium para mujer", "price": 55000, "image_url": "https://placehold.co/400x300/gold/black?text=Versace", "discount": 8, "category": "accesorios-mujer"},
        {"name": "Gorra Nike Mujer", "description": "Gorra deportiva para mujer", "price": 4200, "image_url": "https://placehold.co/400x300/pink/white?text=Nike+Women", "discount": 10, "category": "accesorios-mujer"},
        {"name": "Gorra Adidas Women", "description": "Gorra ajustable para mujer", "price": 3900, "image_url": "https://placehold.co/400x300/pink/white?text=Adidas+Women", "discount": 0, "category": "accesorios-mujer"},
        {"name": "Bolso Michael Kors Tote", "description": "Bolso elegante de cuero", "price": 85000, "image_url": "https://placehold.co/400x300/brown/gold?text=MK+Tote", "discount": 15, "category": "accesorios-mujer"},
        {"name": "Reloj Daniel Wellington", "description": "Reloj minimalista para mujer", "price": 42000, "image_url": "https://placehold.co/400x300/rose/white?text=DW+Watch", "discount": 0, "category": "accesorios-mujer"},
        {"name": "Pañuelo de Seda", "description": "Pañuelo de seda estampado", "price": 15000, "image_url": "https://placehold.co/400x300/purple/white?text=Silk+Scarf", "discount": 5, "category": "accesorios-mujer"},
        {"name": "Cartera Coach Crossbody", "description": "Cartera pequeña crossbody", "price": 65000, "image_url": "https://placehold.co/400x300/brown/white?text=Coach+Bag", "discount": 20, "category": "accesorios-mujer"},
        
        {"name": "Blusa Bershka", "description": "Blusa de verano para mujer", "price": 6500, "image_url": "https://placehold.co/400x300/pink/white?text=Bershka+Blouse", "discount": 5, "category": "blusas"},
        {"name": "Blusa Forever 21", "description": "Blusa estampada moderna", "price": 7200, "image_url": "https://placehold.co/400x300/pink/white?text=F21+Blouse", "discount": 0, "category": "blusas"},
        {"name": "Blusa Zara", "description": "Blusa elegante de seda", "price": 8500, "image_url": "https://placehold.co/400x300/pink/white?text=Zara+Blouse", "discount": 10, "category": "blusas"},
        
        {"name": "Falda H&M", "description": "Falda corta para mujer", "price": 7000, "image_url": "https://placehold.co/400x300/pink/white?text=H%26M+Skirt", "discount": 0, "category": "faldas"},
        {"name": "Falda Midi Zara", "description": "Falda midi plisada", "price": 9000, "image_url": "https://placehold.co/400x300/pink/white?text=Zara+Midi", "discount": 15, "category": "faldas"},
        {"name": "Falda Larga Mango", "description": "Falda larga de verano", "price": 8500, "image_url": "https://placehold.co/400x300/pink/white?text=Mango+Long", "discount": 10, "category": "faldas"},
        
        {"name": "Zapatillas Adidas Mujer", "description": "Zapatillas deportivas para mujer", "price": 17500, "image_url": "https://placehold.co/400x300/white/black?text=Adidas+Women", "discount": 18, "category": "zapatillas"},
        {"name": "Zapatillas Nike Air", "description": "Zapatillas running mujer", "price": 19000, "image_url": "https://placehold.co/400x300/white/black?text=Nike+Air", "discount": 10, "category": "zapatillas"},
        {"name": "Zapatillas Puma Mujer", "description": "Zapatillas casual mujer", "price": 16500, "image_url": "https://placehold.co/400x300/white/black?text=Puma+Women", "discount": 15, "category": "zapatillas"},
        
        {"name": "Bolso Tous", "description": "Bolso elegante para mujer", "price": 22000, "image_url": "https://placehold.co/400x300/brown/gold?text=Tous+Bag", "discount": 12, "category": "bolsos"},
        {"name": "Bolso Michael Kors", "description": "Bolso de cuero premium", "price": 35000, "image_url": "https://placehold.co/400x300/brown/gold?text=MK+Bag", "discount": 8, "category": "bolsos"},
        {"name": "Bolso Coach", "description": "Bolso crossbody elegante", "price": 28000, "image_url": "https://placehold.co/400x300/brown/gold?text=Coach", "discount": 15, "category": "bolsos"},
        
        # Ofertas Especiales
        {"name": "Zapatillas Puma Unisex", "description": "Zapatillas deportivas unisex", "price": 18000, "image_url": "https://placehold.co/400x300/red/white?text=Puma+Sale+40%25", "discount": 40, "category": "ofertas"},
        {"name": "Remera Under Armour", "description": "Remera técnica unisex", "price": 9000, "image_url": "https://placehold.co/400x300/red/white?text=UA+Sale+35%25", "discount": 35, "category": "ofertas"},
        {"name": "Campera North Face", "description": "Campera impermeable unisex", "price": 32000, "image_url": "https://placehold.co/400x300/red/white?text=NF+Sale+45%25", "discount": 45, "category": "ofertas"},
        {"name": "Bolso Deportivo Nike", "description": "Bolso grande unisex", "price": 15000, "image_url": "https://placehold.co/400x300/red/white?text=Nike+Bag+30%25", "discount": 30, "category": "ofertas"},
        {"name": "Zapatillas Nike Air Max", "description": "Zapatillas premium unisex", "price": 25000, "image_url": "https://placehold.co/400x300/red/white?text=Air+Max+35%25", "discount": 35, "category": "ofertas"},
        {"name": "Conjunto Deportivo Adidas", "description": "Conjunto completo unisex", "price": 28000, "image_url": "https://placehold.co/400x300/red/white?text=Adidas+Set+40%25", "discount": 40, "category": "ofertas"},
        {"name": "Mochila The North Face", "description": "Mochila resistente unisex", "price": 20000, "image_url": "https://placehold.co/400x300/red/white?text=TNF+Pack+30%25", "discount": 30, "category": "ofertas"},
        {"name": "Gafas de Sol Ray-Ban", "description": "Gafas de sol clásicas unisex", "price": 22000, "image_url": "https://placehold.co/400x300/red/white?text=RayBan+25%25", "discount": 25, "category": "ofertas"},
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