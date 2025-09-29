"""
Seeder para la carga inicial de usuarios del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlite3 import IntegrityError
from config.cnx import SessionLocal, engine
from config.basemodel import Base
from usuarios.model import Usuario
from roles.model import Rol
from middlewares.auth import hash_password
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_users_table():
    """Crear las tablas de usuarios si no existen"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas de usuarios creadas/verificadas exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise

def seed_usuarios():
    """Cargar usuarios básicos en la base de datos con contraseñas encriptadas usando bcrypt"""
    db = SessionLocal()
    
    print("=== Iniciando carga de usuarios ===")
    print("ℹ️ Las contraseñas se encriptarán usando bcrypt")
    
    try:
        # Obtener IDs de los roles
        rol_admin = db.query(Rol).filter(Rol.rol_nombre == "Administrador").first()
        rol_gerente = db.query(Rol).filter(Rol.rol_nombre == "Gerente").first()
        rol_empleado = db.query(Rol).filter(Rol.rol_nombre == "Empleado").first()
        rol_cajero = db.query(Rol).filter(Rol.rol_nombre == "Cajero").first()
        
        if not rol_admin:
            print("⚠ El rol Administrador debe existir antes de crear usuarios")
            logger.error("❌ El rol Administrador debe existir antes de crear usuarios")
            return
        
        # Definir usuarios del sistema
        usuarios_data = [
            {
                "usu_usuario": "admin",
                "usu_contrasenia": "admin123",
                "usu_nombre_completo": "Administrador del Sistema",
                "usu_rol_id": rol_admin.rol_id
            },
            {
                "usu_usuario": "gerente01",
                "usu_contrasenia": "gerente123",
                "usu_nombre_completo": "María González Gerente",
                "usu_rol_id": rol_gerente.rol_id if rol_gerente else rol_admin.rol_id
            },
            {
                "usu_usuario": "empleado01",
                "usu_contrasenia": "emp123",
                "usu_nombre_completo": "Juan Pérez Empleado",
                "usu_rol_id": rol_empleado.rol_id if rol_empleado else rol_admin.rol_id
            },
            {
                "usu_usuario": "cajero01",
                "usu_contrasenia": "cajero123",
                "usu_nombre_completo": "Ana López Cajera",
                "usu_rol_id": rol_cajero.rol_id if rol_cajero else rol_admin.rol_id
            }
        ]
        
        usuarios_creados = 0
        
        for usuario_info in usuarios_data:
            # Verificar si el usuario ya existe
            existing_usuario = db.query(Usuario).filter(
                Usuario.usu_usuario == usuario_info["usu_usuario"]
            ).first()
            
            if not existing_usuario:
                # Encriptar la contraseña antes de guardarla
                hashed_password = hash_password(usuario_info["usu_contrasenia"])
                
                nuevo_usuario = Usuario(
                    usu_usuario=usuario_info["usu_usuario"],
                    usu_contrasenia=hashed_password,
                    usu_nombre_completo=usuario_info["usu_nombre_completo"],
                    usu_rol_id=usuario_info["usu_rol_id"]
                )
                db.add(nuevo_usuario)
                usuarios_creados += 1
                print(f"✓ Creando usuario: {usuario_info['usu_usuario']} ({usuario_info['usu_nombre_completo']}) - Contraseña encriptada")
                logger.info(f"👤 Creando usuario: {usuario_info['usu_usuario']} ({usuario_info['usu_nombre_completo']})")
            else:
                print(f"- Usuario '{usuario_info['usu_usuario']}' ya existe, omitiendo...")
                logger.info(f"⚠️  Usuario '{usuario_info['usu_usuario']}' ya existe, omitiendo...")
        
        db.commit()
        
        if usuarios_creados > 0:
            print(f"✓ Se crearon {usuarios_creados} usuarios exitosamente")
            logger.info(f"✅ Se crearon {usuarios_creados} usuarios exitosamente")
        else:
            print("ℹ️ Todos los usuarios ya existían")
            logger.info("ℹ️  Todos los usuarios ya existían")
            
    except IntegrityError as e:
        db.rollback()
        print(f"✗ Error de integridad al crear usuarios: {e}")
        logger.error(f"❌ Error de integridad al crear usuarios: {e}")
        raise
    except Exception as e:
        db.rollback()
        print(f"✗ Error inesperado al crear usuarios: {e}")
        logger.error(f"❌ Error inesperado al crear usuarios: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Usuarios ===")
    create_users_table()
    seed_usuarios()
    print("=== Finalizado ===")