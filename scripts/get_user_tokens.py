"""
Script para obtener tokens de todos los usuarios registrados
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.cnx import SessionLocal
from usuarios.model import Usuario
from roles.model import Rol
from config.token import create_access_token
from typing import Dict
import json

def get_all_user_tokens() -> Dict[str, str]:
    """Obtiene los tokens de todos los usuarios registrados"""
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        tokens = {}
        
        for usuario in usuarios:
            # Crear token con el ID del usuario y su rol
            # Obtener el rol directamente del usuario a través de la relación
            # Obtener el rol
            rol = db.query(Rol).filter(Rol.rol_id == usuario.usu_rol_id).first()
            token_data = {
                "sub": str(usuario.usu_id),
                "username": usuario.usu_usuario,
                "role": rol.rol_nombre if rol else "unknown"
            }
            token = create_access_token(token_data)
            tokens[usuario.usu_usuario] = {
                "token": token,
                "nombre_completo": usuario.usu_nombre_completo,
                "rol": token_data["role"]
            }
        
        return tokens
    finally:
        db.close()

if __name__ == "__main__":
    print("\n=== Tokens de Usuarios ===\n")
    tokens = get_all_user_tokens()
    
    # Imprimir tokens en formato JSON bonito
    print(json.dumps(tokens, indent=2, ensure_ascii=False))
    print("\n=== Fin ===\n")