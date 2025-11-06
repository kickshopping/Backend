"""
Genera y muestra un token JWT para el usuario admin en la DB y su payload.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from usuarios.model import Usuario
from usuarios.services import create_access_token
from config.auth import SECRET_KEY, ALGORITHM
import jwt


def show_token():
    db = SessionLocal()
    try:
        admin = db.query(Usuario).filter(Usuario.usu_usuario == 'admin@gmail.com').first()
        if not admin:
            print('Usuario admin no encontrado')
            return
        data = {"sub": admin.usu_usuario, "rol_id": admin.usu_rol_id, "user_id": admin.usu_id}
        token = create_access_token(data)
        print('\n=== Access Token (compact) ===')
        print(token)
        print('\n=== Decoded payload ===')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)
        except Exception as e:
            print('Error al decodificar token:', e)
    finally:
        db.close()

if __name__ == '__main__':
    show_token()
