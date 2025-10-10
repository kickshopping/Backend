
"""
Seeder de productos de ropa para hombre, mujer y unisex, organizado por secciones.
"""
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from productos.model import Product

def seed_productos():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    productos = [
        # Hombre
        Product(name="Calzón Calvin Klein", description="Calzón cómodo para hombre", price=3500, image_url="/buzo.jpeg", discount=5),
        Product(name="Gorra Nike", description="Gorra deportiva para hombre", price=4000, image_url="/buzo.jpeg", discount=10),
        Product(name="Campera North Face", description="Campera impermeable para hombre", price=25000, image_url="/buzo.jpeg", discount=15),
        Product(name="Buzo Adidas", description="Buzo de algodón para hombre", price=12000, image_url="/buzo.jpeg", discount=10),
        Product(name="Pantalón Levis", description="Pantalón de jean para hombre", price=11000, image_url="/buzo.jpeg", discount=10),
        Product(name="Remera Nike", description="Remera deportiva para hombre", price=8000, image_url="/buzo.jpeg", discount=5),
        Product(name="Camisa Zara", description="Camisa casual para hombre", price=9500, image_url="/buzo.jpeg", discount=0),
        Product(name="Zapatillas Puma", description="Zapatillas deportivas para hombre", price=18000, image_url="/buzo.jpeg", discount=20),

        # Mujer
        Product(name="Vestido Mango", description="Vestido elegante para mujer", price=15000, image_url="/buzo.jpeg", discount=15),
        Product(name="Blusa Bershka", description="Blusa de verano para mujer", price=6500, image_url="/buzo.jpeg", discount=5),
        Product(name="Falda H&M", description="Falda corta para mujer", price=7000, image_url="/buzo.jpeg", discount=0),
        Product(name="Pantalón Stradivarius", description="Pantalón de vestir para mujer", price=10500, image_url="/buzo.jpeg", discount=8),
        Product(name="Remera Zara Mujer", description="Remera básica para mujer", price=7500, image_url="/buzo.jpeg", discount=5),
        Product(name="Zapatillas Adidas Mujer", description="Zapatillas deportivas para mujer", price=17500, image_url="/buzo.jpeg", discount=18),
        Product(name="Bolso Tous", description="Bolso elegante para mujer", price=22000, image_url="/buzo.jpeg", discount=12),
        Product(name="Accesorio Pandora", description="Pulsera de plata para mujer", price=9000, image_url="/buzo.jpeg", discount=10),

        # Unisex
        Product(name="Pantalón Levis Unisex", description="Pantalón de jean unisex", price=11000, image_url="/buzo.jpeg", discount=10),
        Product(name="Remera Unisex", description="Remera básica unisex", price=7000, image_url="/buzo.jpeg", discount=5),
        Product(name="Zapatillas Puma Unisex", description="Zapatillas deportivas unisex", price=18000, image_url="/buzo.jpeg", discount=20),
        Product(name="Bolso Unisex", description="Bolso casual unisex", price=15000, image_url="/buzo.jpeg", discount=10),
        Product(name="Accesorio Unisex", description="Collar de acero unisex", price=6000, image_url="/buzo.jpeg", discount=8),
    ]
    db.add_all(productos)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_productos()