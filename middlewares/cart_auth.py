from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config.auth import SECRET_KEY, ALGORITHM
from config.cnx import SessionLocal
from usuarios.model import Usuario
from roles.model import Rol

security = HTTPBearer()

def verify_token_and_permissions(credentials: HTTPAuthorizationCredentials = Security(security), required_permission: str = None) -> dict:
    """
    Verifica el token JWT y los permisos del usuario
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if "user_id" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
            
        # Si no se requiere un permiso específico, solo validamos el token
        if not required_permission:
            return payload
            
        # Verificar permisos
        db = SessionLocal()
        try:
            user = db.query(Usuario).filter(Usuario.usu_id == payload["user_id"]).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
                
            # Verificar permisos a través del rol del usuario
            role = db.query(Rol).filter(Rol.rol_id == user.rol_id).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario sin rol asignado"
                )
                
            # Verificar si el rol tiene el permiso requerido
            has_permission = any(
                getattr(permiso, 'permiso_nombre', None) == required_permission
                for permiso in role.permisos
            )
            
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"No tienes permiso para realizar esta acción"
                )
                
            return payload
            
        finally:
            db.close()
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar permisos: {str(e)}"
        )