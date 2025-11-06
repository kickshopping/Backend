"""
Script para actualizar los permisos del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seeders.seed_permisos import create_permissions_table, seed_permisos
from seeders.seed_roles import create_roles_table
from seeders.seed_rol_permisos import seed_rol_permisos

def main():
    print("=== Iniciando actualización de permisos ===")
    
    # 1. Asegurar tablas
    create_permissions_table()
    create_roles_table()
    
    # 2. Cargar permisos
    seed_permisos()
    
    # 3. Asignar permisos a roles
    seed_rol_permisos()
    
    print("=== Actualización completada ===")

if __name__ == "__main__":
    main()