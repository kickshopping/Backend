from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from contextlib import contextmanager

from config.database import DATABASE_URL

# Crear el motor de la base de datos
# echo=True solo en desarrollo para ver las consultas SQL
engine = create_engine(DATABASE_URL, echo=False)

# Configurar la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency que proporciona una sesión de base de datos para FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Administrador de contexto para usar la base de datos fuera de FastAPI
    
    Ejemplo:
        with get_db_context() as db:
            user = db.query(User).first()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()