import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from permisos.model import Permiso
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_admin_permisos():
    """Cargar permisos de administrador para gestión de productos"""
    db = SessionLocal()
    
    print("=== Iniciando carga de permisos de administrador ===")
    
    permisos_admin = [
        {
            "permiso_nombre": "crear_producto",
            "permiso_ruta": "/productos",
            "permiso_metodo": "POST",
            "permiso_descripcion": "Crear nuevos productos"
        },
        {
            "permiso_nombre": "editar_producto",
            "permiso_ruta": "/productos/{id}",
            "permiso_metodo": "PUT",
            "permiso_descripcion": "Editar productos existentes"
        },
        {
            "permiso_nombre": "eliminar_producto",
            "permiso_ruta": "/productos/{id}",
            "permiso_metodo": "DELETE",
            "permiso_descripcion": "Eliminar productos"
        },
        {
            "permiso_nombre": "ver_todos_productos",
            "permiso_ruta": "/productos/admin",
            "permiso_metodo": "GET",
            "permiso_descripcion": "Ver lista completa de productos con opciones de administración"
        }
    ]
    
    try:
        permisos_creados = 0
        
        for permiso_info in permisos_admin:
            # Verificar si el permiso ya existe
            existing_permiso = db.query(Permiso).filter(
                Permiso.permiso_nombre == permiso_info["permiso_nombre"]
            ).first()
            
            if not existing_permiso:
                nuevo_permiso = Permiso(**permiso_info)
                db.add(nuevo_permiso)
                permisos_creados += 1
                print(f"✓ Creando permiso: {permiso_info['permiso_nombre']}")
                logger.info(f"📝 Creando permiso: {permiso_info['permiso_nombre']}")
            else:
                print(f"- Permiso '{permiso_info['permiso_nombre']}' ya existe, omitiendo...")
                logger.info(f"⚠️ Permiso '{permiso_info['permiso_nombre']}' ya existe")
        
        db.commit()
        
        if permisos_creados > 0:
            print(f"✓ Se crearon {permisos_creados} permisos exitosamente")
            logger.info(f"✅ Se crearon {permisos_creados} permisos exitosamente")
        else:
            print("ℹ️ Todos los permisos ya existían")
            logger.info("ℹ️ Todos los permisos ya existían")
            
    except Exception as e:
        db.rollback()
        print(f"✗ Error al crear permisos: {e}")
        logger.error(f"❌ Error al crear permisos: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Permisos de Administrador ===")
    seed_admin_permisos()
    print("=== Finalizado ===")