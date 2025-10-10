"""
Configuración centralizada de tablas para evitar problemas de orden de importación
"""
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from config.basemodel import Base

# Definir la tabla intermedia aquí para evitar problemas de importación circular
rol_permiso_association = Table(
    'rol_permiso', 
    Base.metadata,
    Column('rol_id', Integer, ForeignKey('roles.rol_id'), primary_key=True),
    Column('permiso_id', Integer, ForeignKey('permisos.permiso_id'), primary_key=True), 
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)