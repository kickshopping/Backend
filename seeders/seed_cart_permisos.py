"""
Seeder para la carga de permisos relacionados con el carrito
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from sqlalchemy.exc import IntegrityError
from config.cnx import SessionLocal
from permisos.model import Permiso
from roles.model import Rol
from config.associations import rol_permiso_association

def seed_cart_permisos():
    """Crear permisos relacionados con el carrito"""
    db = SessionLocal()
    
    try:
        print("=== Iniciando carga de permisos del carrito ===")
        
        # Definir permisos del carrito
        cart_permissions = [
            {
                "permiso_nombre": "eliminar_item_carrito",
                "permiso_descripcion": "Permite eliminar items del carrito propio",
                "permiso_ruta": "/cart_items/{cart_item_id}",
                "permiso_metodo": "DELETE",
                "permiso_activo": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "permiso_nombre": "ver_carrito",
                "permiso_descripcion": "Permite ver el carrito propio",
                "permiso_ruta": "/cart_items/user/{user_id}",
                "permiso_metodo": "GET",
                "permiso_activo": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "permiso_nombre": "modificar_carrito",
                "permiso_descripcion": "Permite modificar cantidades en el carrito propio",
                "permiso_ruta": "/cart_items/{cart_item_id}",
                "permiso_metodo": "PUT",
                "permiso_activo": True,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
                ,
                {
                    "permiso_nombre": "incrementar_carrito",
                    "permiso_descripcion": "Permite incrementar la cantidad de un item del carrito",
                    "permiso_ruta": "/cart_items/{cart_item_id}/increment",
                    "permiso_metodo": "POST",
                    "permiso_activo": True,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                },
                {
                    "permiso_nombre": "decrementar_carrito",
                    "permiso_descripcion": "Permite decrementar la cantidad de un item del carrito",
                    "permiso_ruta": "/cart_items/{cart_item_id}/decrement",
                    "permiso_metodo": "POST",
                    "permiso_activo": True,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
        ]
        
        # Crear los permisos
        created_permissions = []
        for perm in cart_permissions:
            try:
                # Verificar si el permiso ya existe
                existing = db.query(Permiso).filter_by(permiso_nombre=perm["permiso_nombre"]).first()
                if not existing:
                    new_perm = Permiso(**perm)
                    db.add(new_perm)
                    db.flush()  # Para obtener el ID
                    created_permissions.append(new_perm)
                    print(f"✓ Permiso creado: {perm['permiso_nombre']}")
                else:
                    print(f"• Permiso ya existe: {perm['permiso_nombre']}")
                    created_permissions.append(existing)
            except IntegrityError:
                db.rollback()
                print(f"✗ Error al crear permiso: {perm['permiso_nombre']}")
                continue
        
        # Asignar permisos al rol de comprador
        comprador_role = db.query(Rol).filter_by(rol_nombre="comprador").first()
        if comprador_role:
            for permission in created_permissions:
                # Verificar si la asociación ya existe
                exists = db.query(rol_permiso_association).filter_by(
                    rol_id=comprador_role.rol_id,
                    per_id=permission.permiso_id
                ).first()
                
                if not exists:
                    # Crear la asociación
                    comprador_role.permisos.append(permission)
                    print(f"✓ Permiso {permission.permiso_nombre} asignado al rol comprador")
                else:
                    print(f"• Permiso {permission.permiso_nombre} ya asignado al rol comprador")
        
        db.commit()
        print("=== Carga de permisos del carrito completada ===")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error durante la carga de permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_cart_permisos()