"""
Seeder para la asignación de permisos a roles
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy import text
from config.cnx import SessionLocal
from permisos.model import Permiso
from roles.model import Rol

def seed_rol_permisos():
    """Asignar permisos a roles existentes"""
    db = SessionLocal()
    
    try:
        print("=== Iniciando asignación de permisos a roles ===")
        
        # Obtener roles existentes
        roles = db.query(Rol).all()
        
        if not roles:
            print("⚠ No hay roles en el sistema. Ejecute primero el seeder de roles.")
            return
        
        # Obtener todos los permisos
        permisos = db.query(Permiso).all()
        permisos_dict = {}
        for p in permisos:
            permisos_dict[p.permiso_nombre] = p.permiso_id
        
        # Definir asignaciones de permisos por rol - ACTUALIZADAS según rutas reales
        rol_permisos_config = {
            "administrador": [
                # === PERMISOS COMPLETOS DE ADMINISTRADOR ===
                # Usuarios
                "usuarios.listar", "usuarios.crear", "usuarios.ver_perfil", "usuarios.ver", 
                "usuarios.actualizar", "usuarios.eliminar", "usuarios.login",
                # Roles
                "roles.listar", "roles.crear", "roles.ver", "roles.actualizar", "roles.eliminar",
                # Productos
                "productos.listar", "productos.crear", "productos.ver", "productos.actualizar", "productos.eliminar",
                # Carrito
                "cart_items.listar", "cart_items.ver_usuario", "cart_items.ver", "cart_items.crear",
                "cart_items.actualizar", "cart_items.eliminar", "cart_items.limpiar_carrito",
                # Permisos (meta-administración)
                "permisos.listar", "permisos.crear", "permisos.ver", "permisos.actualizar", 
                "permisos.eliminar", "permisos.asignar_rol", "permisos.remover_rol"
            ],
            "gerente": [
                # === PERMISOS DE GESTIÓN PARA GERENTE ===
                # Usuarios (solo lectura y actualización)
                "usuarios.listar", "usuarios.ver_perfil", "usuarios.ver", "usuarios.actualizar", "usuarios.login",
                # Roles (solo lectura)
                "roles.listar", "roles.ver",
                # Productos (gestión completa)
                "productos.listar", "productos.crear", "productos.ver", "productos.actualizar", "productos.eliminar",
                # Carrito (gestión completa)
                "cart_items.listar", "cart_items.ver_usuario", "cart_items.ver", "cart_items.crear",
                "cart_items.actualizar", "cart_items.eliminar", "cart_items.limpiar_carrito",
                # Permisos (solo lectura)
                "permisos.listar", "permisos.ver"
            ],
            "empleado": [
                # === PERMISOS BÁSICOS PARA EMPLEADO ===
                # Usuarios (solo perfil propio)
                "usuarios.ver_perfil", "usuarios.login",
                # Productos (solo lectura)
                "productos.listar", "productos.ver",
                # Carrito (gestión básica)
                "cart_items.listar", "cart_items.ver_usuario", "cart_items.ver", "cart_items.crear",
                "cart_items.actualizar", "cart_items.eliminar"
            ],
            "cliente": [
                # === PERMISOS PARA CLIENTE ===
                # Usuarios (perfil propio y login)
                "usuarios.ver_perfil", "usuarios.actualizar", "usuarios.login",
                # Productos (solo lectura)
                "productos.listar", "productos.ver",
                # Carrito (gestión de su propio carrito)
                "cart_items.ver_usuario", "cart_items.ver", "cart_items.crear",
                "cart_items.actualizar", "cart_items.eliminar", "cart_items.limpiar_carrito"
            ]
        }
        
        asignaciones_realizadas = 0
        
        for rol in roles:
            rol_nombre = rol.rol_nombre.lower()
            
            if rol_nombre in rol_permisos_config:
                # Limpiar asignaciones existentes para este rol
                delete_sql = text("DELETE FROM rol_permiso WHERE rol_id = :rol_id")
                db.execute(delete_sql, {"rol_id": rol.rol_id})
                
                # Asignar nuevos permisos
                permisos_rol = rol_permisos_config[rol_nombre]
                
                permisos_asignados = 0
                for permiso_nombre in permisos_rol:
                    if permiso_nombre in permisos_dict:
                        permiso_id = permisos_dict[permiso_nombre]
                        insert_sql = text("""
                            INSERT INTO rol_permiso (rol_id, permiso_id, created_at) 
                            VALUES (:rol_id, :permiso_id, :created_at)
                        """)
                        db.execute(insert_sql, {
                            "rol_id": rol.rol_id,
                            "permiso_id": permiso_id,
                            "created_at": datetime.utcnow()
                        })
                        permisos_asignados += 1
                        asignaciones_realizadas += 1
                    else:
                        print(f"⚠ Permiso '{permiso_nombre}' no encontrado")
                
                print(f"✓ Asignados {permisos_asignados} permisos al rol '{rol.rol_nombre}'")
            else:
                print(f"⚠ No hay configuración de permisos para el rol '{rol.rol_nombre}'")
        
        db.commit()
        print(f"\n✓ {asignaciones_realizadas} asignaciones de permisos realizadas correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error al asignar permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Seeder de Asignación Rol-Permisos ===")
    seed_rol_permisos()
    print("=== Finalizado ===")