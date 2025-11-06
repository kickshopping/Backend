from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config.auth import ALGORITHM, SECRET_KEY
from usuarios.model import Usuario
from config.cnx import SessionLocal
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_admin(token: str = Depends(oauth2_scheme)):
    """Verificar que el usuario sea administrador"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    # Tratar distintas formas de claims en el JWT: 'sub', 'user_id', 'userId'
    user_id = None
    try:
        sub = payload.get("sub")
        if sub is not None:
            # sub puede ser un número (id) o un string (email). Intentar convertir a int.
            try:
                user_id = int(sub)
            except Exception:
                # dejar user_id como None; luego intentaremos buscar por email/username
                user_id = None

        if user_id is None:
            user_id = payload.get("user_id") or payload.get("userId")
            if isinstance(user_id, str) and user_id.isdigit():
                user_id = int(user_id)
    except Exception:
        # en caso de payload inesperado
        user_id = None
    
    db = SessionLocal()
    try:
        user = None
        # Buscar por id si lo tenemos
        if user_id is not None:
            user = db.query(Usuario).filter(Usuario.usu_id == user_id).first()

        # Si no encontramos por id, intentar buscar por nombre de usuario/email en 'sub' o en claims comunes
        if not user:
            # posibles claves con nombre de usuario
            username = payload.get('username') or payload.get('usu_usuario') or payload.get('email') or payload.get('sub')
            if isinstance(username, str) and username:
                user = db.query(Usuario).filter(Usuario.usu_usuario == username).first()

        if not user:
            raise credentials_exception

        # Verificar si el usuario tiene el rol de administrador
        # El modelo Usuario define la relación como `rol` (no usu_rol)
        if not getattr(user, 'rol', None) or user.rol.rol_nombre != "Administrador":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Se requieren privilegios de administrador"
            )
        
        return user
    finally:
        db.close()