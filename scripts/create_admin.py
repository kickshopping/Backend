"""
Script para crear el usuario admin directamente
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from datetime import datetime
from middlewares.auth import hash_password

def create_admin():
    try:
        # Conectar directamente a la base de datos SQLite
        conn = sqlite3.connect('mise_db')
        cursor = conn.cursor()
        
        # Verificar si el rol de administrador existe
        cursor.execute("SELECT rol_id FROM roles WHERE rol_nombre = ?", ("Administrador",))
        rol = cursor.fetchone()
        
        if not rol:
            print("❌ El rol de Administrador no existe")
            return
            
        rol_id = rol[0]
        
        # Verificar si el usuario admin ya existe
        cursor.execute("SELECT usu_id FROM usuarios WHERE usu_usuario = ?", ("admin@gmail.com",))
        if cursor.fetchone():
            print("⚠️ El usuario admin ya existe")
            return
        
        # Crear el usuario admin
        hashed_password = hash_password("admin123")
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            INSERT INTO usuarios (
                usu_usuario,
                usu_contrasenia,
                usu_rol_id,
                usu_nombre_completo,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "admin@gmail.com",
            hashed_password,
            rol_id,
            "Administrador del Sistema",
            now,
            now
        ))
        
        conn.commit()
        print("✅ Usuario admin creado exitosamente")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_admin()