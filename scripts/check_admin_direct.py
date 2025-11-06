"""
Script para verificar el usuario admin y su rol de manera directa
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3

def check_admin():
    try:
        # Conectar directamente a la base de datos SQLite
        conn = sqlite3.connect('mise_db')
        cursor = conn.cursor()
        
        # Obtener información del usuario admin y su rol
        cursor.execute("""
            SELECT u.usu_id, u.usu_usuario, u.usu_nombre_completo, u.usu_rol_id, r.rol_nombre
            FROM usuarios u
            LEFT JOIN roles r ON u.usu_rol_id = r.rol_id
            WHERE u.usu_usuario = ?
        """, ("admin@gmail.com",))
        
        admin = cursor.fetchone()
        
        if admin:
            print("\n=== Usuario Admin ===")
            print(f"ID: {admin[0]}")
            print(f"Usuario: {admin[1]}")
            print(f"Nombre: {admin[2]}")
            print(f"Rol ID: {admin[3]}")
            print(f"Rol Nombre: {admin[4]}")
            print("==================")
        else:
            print("\n❌ Usuario admin no encontrado")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_admin()