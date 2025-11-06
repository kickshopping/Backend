"""
Script para crear el rol de Administrador directamente
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
from datetime import datetime

def create_admin_role():
    try:
        # Conectar directamente a la base de datos SQLite
        conn = sqlite3.connect('mise_db')
        cursor = conn.cursor()
        
        # Verificar si el rol ya existe
        cursor.execute("SELECT rol_id FROM roles WHERE rol_nombre = ?", ("Administrador",))
        if cursor.fetchone():
            print("⚠️ El rol Administrador ya existe")
            return
            
        # Crear el rol de administrador
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            INSERT INTO roles (
                rol_nombre,
                created_at,
                updated_at
            ) VALUES (?, ?, ?)
        """, (
            "Administrador",
            now,
            now
        ))
        
        conn.commit()
        print("✅ Rol Administrador creado exitosamente")
            
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_admin_role()