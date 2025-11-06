import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import STRCNX
from config.cnx import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Verificar la tabla de usuarios
    res = conn.execute(text("SELECT usu_id, usu_usuario, usu_nombre_completo, usu_contrasenia FROM usuarios"))
    print('\nUsuarios en la base de datos:')
    print('-----------------------------')
    for user in res.fetchall():
        print(f'ID: {user[0]}')
        print(f'Usuario: {user[1]}')
        print(f'Nombre Completo: {user[2]}')
        print(f'Hash de Contraseña: {user[3][:20]}...') # Solo mostramos parte del hash por seguridad
        print('-----------------------------')