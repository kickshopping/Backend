import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.cnx import SessionLocal
from roles.model import Rol
from permisos.model import Permiso

def assign_cart_perms_to_vendedor():
    db = SessionLocal()
    try:
        vendedor = db.query(Rol).filter(Rol.rol_id == 1).first()
        if not vendedor:
            print("No se encontró el rol con rol_id=1 (Vendedor)")
            return

        cart_perms = [
            "cart_items.ver_usuario",
            "cart_items.ver",
            "cart_items.crear",
            "cart_items.actualizar",
            "cart_items.eliminar",
            "cart_items.limpiar_carrito",
            "eliminar_item_carrito",
            "ver_carrito",
            "modificar_carrito",
            "incrementar_carrito",
            "decrementar_carrito"
        ]

        added = 0
        for perm_name in cart_perms:
            perm = db.query(Permiso).filter(Permiso.permiso_nombre == perm_name).first()
            if not perm:
                print(f"Permiso no encontrado en la BD: {perm_name}")
                continue
            # asociar si no existe
            if perm not in vendedor.permisos:
                vendedor.permisos.append(perm)
                added += 1
                print(f"Asignando permiso {perm_name} a Vendedor")
            else:
                print(f"Permiso ya asignado: {perm_name}")

        if added > 0:
            db.commit()
            print(f"Se asignaron {added} permisos al rol Vendedor")
        else:
            print("No se asignaron permisos nuevos (ya estaban presentes o faltaban permisos en la BD)")

    except Exception as e:
        db.rollback()
        print("Error al asignar permisos:", e)
    finally:
        db.close()

if __name__ == '__main__':
    assign_cart_perms_to_vendedor()
