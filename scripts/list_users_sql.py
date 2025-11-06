"""
Script para listar los usuarios registrados usando SQL directo
"""
import os
import sqlite3

def list_users():
    """Lista todos los usuarios registrados"""
    try:
        # Conectar a la base de datos SQLite
        db_path = os.path.join(os.getcwd(), 'mise_db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener usuarios con sus roles
        cursor.execute("""
            SELECT u.usu_id, u.usu_usuario, u.usu_nombre_completo, r.rol_nombre 
            FROM usuarios u 
            JOIN roles r ON u.usu_rol_id = r.rol_id
        """)
        
        users = cursor.fetchall()
        
        print("\n=== Usuarios Registrados ===\n")
        for user in users:
            print(f"ID: {user[0]}")
            print(f"Usuario: {user[1]}")
            print(f"Nombre Completo: {user[2]}")
            print(f"Rol: {user[3]}")
            print("-" * 50)
            
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_users()
    print("\n=== Fin ===\n")