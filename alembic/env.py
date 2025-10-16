"""
Configuración de Alembic para migraciones de la base de datos.
Permite crear y actualizar las tablas según los modelos definidos.
"""

import sys  # Acceso a argumentos y rutas del sistema
import os  # Acceso a variables de entorno y rutas
from logging.config import fileConfig  # Configuración de logging
from sqlalchemy import engine_from_config, pool  # Herramientas de SQLAlchemy
from alembic import context  # Contexto de Alembic

# Configuración de logging para migraciones
fileConfig(context.config.config_file_name)

# Agrega la ruta del proyecto para importar modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la base de los modelos
from cart.models.cart_models import Base

# Configura la URL de la base de datos (por defecto SQLite local)
config = context.config
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL', 'sqlite:///./kickshopping.db'))

target_metadata = Base.metadata  # Metadatos de los modelos para migraciones

def run_migrations_offline():
    """
    Ejecuta migraciones en modo offline (sin conexión directa).
    """
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Ejecuta migraciones en modo online (con conexión directa).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Determina el modo de ejecución y corre las migraciones
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
