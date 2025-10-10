from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from config.basemodel import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    usu_id = Column (Integer, primary_key=True, autoincrement=True)
    usu_usuario = Column (String (50), nullable=False, unique=True)
    usu_contrasenia = Column (String(255), nullable=False)  # Ampliado para soportar hashing
    usu_rol_id = Column (Integer, ForeignKey("roles.rol_id"), nullable=False) 
    usu_nombre_completo = Column (String (100), nullable=False)  # Ampliado para nombres completos
    birthdate = Column(Date, nullable=True)  # Nueva columna para fecha de nacimiento
    created_at = Column (DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relación con rol (las ventas se definen en el modelo Venta)
    rol = relationship("Rol", backref="usuarios")
    
