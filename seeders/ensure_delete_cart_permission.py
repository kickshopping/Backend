import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from roles.model import Rol
from permisos.model import Permiso
from config.associations import rol_permiso_association

def ensure_delete_cart_permission():
    db = SessionLocal()
    try:
        # 1. Asegurarse de que existe el permiso
        delete_perm = db.query(Permiso).filter(Permiso.permiso_nombre == "cart_items.eliminar").first()
        if not delete_perm:
            print("Creando permiso cart_items.eliminar...")
            delete_perm = Permiso(
                permiso_nombre="cart_items.eliminar",
                permiso_ruta="/cart_items/{id}",
                permiso_metodo="DELETE",
                permiso_descripcion="Eliminar elemento del carrito"
            )
            db.add(delete_perm)
            db.commit()
            db.refresh(delete_perm)
        
        # 2. Obtener todos los roles
        roles = db.query(Rol).all()
        
        # 3. Asignar el permiso a todos los roles que no lo tengan
        for rol in roles:
            # Verificar si el rol ya tiene el permiso
            has_perm = db.query(rol_permiso_association).filter_by(
                rol_id=rol.rol_id,
                permiso_id=delete_perm.permiso_id
            ).first()
            
            if not has_perm:
                print(f"Asignando permiso de eliminar items del carrito al rol: {rol.rol_nombre}")
                # Agregar la asociación
                stmt = rol_permiso_association.insert().values(
                    rol_id=rol.rol_id,
                    permiso_id=delete_perm.permiso_id
                )
                db.execute(stmt)
        
        db.commit()
        print("Proceso completado exitosamente")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    ensure_delete_cart_permission()