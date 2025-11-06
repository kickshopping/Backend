import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.cnx import engine
from config.basemodel import Base
from roles.model import Rol
from usuarios.model import Usuario
from cart_items.model import CartItem
from productos.model import Product

print("Eliminando tablas...")
CartItem.__table__.drop(engine, checkfirst=True)
Usuario.__table__.drop(engine, checkfirst=True)
Product.__table__.drop(engine, checkfirst=True)
Rol.__table__.drop(engine, checkfirst=True)

print("Recreando tablas...")
Base.metadata.create_all(engine)

print("¡Base de datos reiniciada!")