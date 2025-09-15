"""
Archivo que define la base declarativa para los modelos de SQLAlchemy.
Permite que todos los modelos hereden de 'Base' para la creación de tablas.
"""

from sqlalchemy.orm import declarative_base  # Importa la función para crear la base declarativa

# Instancia la base para que los modelos la hereden
Base = declarative_base()
