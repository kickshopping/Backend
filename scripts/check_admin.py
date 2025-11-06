"""
Script para verificar el usuario admin y su rol
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from usuarios.model import Usuario
from roles.model import Rol

def check_admin():
    db = SessionLocal()
    try:
        # Obtener el usuario admin
        admin = db.query(Usuario).filter(Usuario.usu_usuario == "admin@gmail.com").first()
        if admin:
            # Obtener el rol del admin
            rol = db.query(Rol).filter(Rol.rol_id == admin.usu_rol_id).first()
            print("\n=== Usuario Admin ===")
            print(f"ID: {admin.usu_id}")
            print(f"Usuario: {admin.usu_usuario}")
            print(f"Nombre: {admin.usu_nombre_completo}")
            print(f"Rol ID: {admin.usu_rol_id}")
            print(f"Rol Nombre: {rol.rol_nombre if rol else 'No encontrado'}")
            print("==================")
        else:
            print("\n❌ Usuario admin no encontrado")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin()