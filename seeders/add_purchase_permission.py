import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from roles.model import Rol
from permisos.model import Permiso

def add_purchase_permission():
    db = SessionLocal()
    try:
        # Crear el permiso de compra si no existe
        purchase_permission = db.query(Permiso).filter(
            Permiso.permiso_nombre == "cart_items.purchase"
        ).first()

        if not purchase_permission:
            purchase_permission = Permiso(
                permiso_nombre="cart_items.purchase",
                permiso_ruta="/cart_items/purchase",
                permiso_metodo="POST",
                permiso_descripcion="Realizar compra de items en el carrito"
            )
            db.add(purchase_permission)
            db.commit()
            print("✓ Permiso de compra creado exitosamente")
        else:
            print("• Permiso de compra ya existe")

        # Roles que deberían tener permiso de compra
        roles_to_update = ["cliente", "comprador", "administrador", "gerente"]
        
        for rol_nombre in roles_to_update:
            rol = db.query(Rol).filter(Rol.rol_nombre == rol_nombre).first()
            if rol:
                if purchase_permission not in rol.permisos:
                    rol.permisos.append(purchase_permission)
                    print(f"✓ Permiso de compra asignado al rol {rol_nombre}")
                else:
                    print(f"• Rol {rol_nombre} ya tiene el permiso de compra")
        
        db.commit()
        print("=== Asignación de permisos de compra completada ===")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error durante la asignación de permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_purchase_permission()