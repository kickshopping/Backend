"""
Archivo de configuración de la conexión a la base de datos.
Define el engine y la sesión para SQLAlchemy usando SQLite por defecto.
"""

import os  # Importa el módulo para acceder a variables de entorno
from sqlalchemy import create_engine  # Importa la función para crear el engine de SQLAlchemy
from sqlalchemy.orm import sessionmaker  # Importa el constructor de sesiones

# Obtiene la URL de la base de datos desde la variable de entorno o usa SQLite local por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kickshopping.db")

# Crea el engine de SQLAlchemy para conectarse a la base de datos
engine = create_engine(
    DATABASE_URL,  # URL de la base de datos
    connect_args={"check_same_thread": False}  # Argumento necesario para SQLite en modo multihilo
)

# Crea la clase SessionLocal para instanciar sesiones de base de datos
SessionLocal = sessionmaker(
    autocommit=False,  # No autocommit para mayor control
    autoflush=False,   # No autoflush para evitar escrituras automáticas
    bind=engine        # Asocia la sesión al engine creado
)


