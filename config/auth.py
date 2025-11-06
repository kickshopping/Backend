from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from typing import Any, Dict
from jose import jwt

load_dotenv()

# Configuración de autenticación
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    # No bloquear la importación en desarrollo; usar valor por defecto y avisar
    SECRET_KEY = 'dev-secret-change-me'
    print("[config.auth] WARNING: SECRET_KEY no está definida en .env — usando clave por defecto de desarrollo")

ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '30'))