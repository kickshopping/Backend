"""
Script para listar los usuarios registrados
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from usuarios.model import Usuario

def list_users():
    """Lista todos los usuarios registrados"""
    db = SessionLocal()
    try:
        print("\n=== Usuarios Registrados ===\n")
        usuarios = db.query(Usuario).all()
        
        for usuario in usuarios:
            print(f"\nID: {usuario.usu_id}")
            print(f"Usuario: {usuario.usu_usuario}")
            print(f"Nombre Completo: {usuario.usu_nombre_completo}")
            print(f"Rol ID: {usuario.usu_rol_id}")
            print("-" * 50)
            
    finally:
        db.close()

if __name__ == "__main__":
    list_users()
    print("\n=== Fin ===\n")