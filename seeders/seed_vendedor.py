import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.cnx import SessionLocal
from middlewares.auth import hash_password
from usuarios.model import Usuario
from roles.model import Rol
from permisos.model import Permiso

def seed_vendedor():
    import datetime
    db = SessionLocal()
    try:
        # Cambia estos datos si quieres otro usuario vendedor
        # Actualizar el usuario con usu_id=1 para que sea vendedor
        user = db.query(Usuario).filter(Usuario.usu_id == 1).first()
        if not user:
            print("No se encontró el usuario con usu_id=1.")
            return
        user.usu_rol_id = 1
        db.commit()
        print("Usuario con usu_id=1 actualizado a vendedor (rol_id=1)")
    except Exception as e:
        db.rollback()
        print("Error creando usuario vendedor:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_vendedor()
