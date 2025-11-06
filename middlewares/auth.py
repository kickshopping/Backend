from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Set
from fastapi import HTTPException, Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt
import bcrypt

from config.auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class RouteConfig:
    """Configuración de rutas públicas y protegidas"""
    PUBLIC_ROUTES: Set[str] = {
        "/",
        "/home",
        "/test",
        "/health",
        "/docs",
        "/debug/dbinfo",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    }

    PUBLIC_METHODS: Dict[str, List[str]] = {
        "/usuarios": ["POST"],
        "/usuarios/login": ["POST"],
        "/productos": ["GET", "POST"],
        "/productos/": ["GET", "POST"],
        "/cart_items": ["GET", "POST"],
        "/cart_items/": ["GET", "POST"],
    }

    PUBLIC_PATH_PREFIXES: List[str] = [
        "/static/",
        "/productos/categoria/",
    ]

    AUTHENTICATED_ONLY_ROUTES: List[str] = [
        "/usuarios/me",
        "/cart_items/me",
        # Permitir que cualquier usuario autenticado finalice compras sin permiso adicional
        "/cart_items/purchase",
    ]

    @classmethod
    def is_public_route(cls, path: str, method: str) -> bool:
        if path in cls.PUBLIC_ROUTES:
            return True
        if any(path.startswith(prefix) for prefix in cls.PUBLIC_PATH_PREFIXES):
            return True
        if path in cls.PUBLIC_METHODS and method in cls.PUBLIC_METHODS[path]:
            return True
        return False


# Exponer constantes a nivel de módulo para compatibilidad
PUBLIC_ROUTES = RouteConfig.PUBLIC_ROUTES
PUBLIC_METHODS = RouteConfig.PUBLIC_METHODS
PUBLIC_PATH_PREFIXES = RouteConfig.PUBLIC_PATH_PREFIXES
AUTHENTICATED_ONLY_ROUTES = RouteConfig.AUTHENTICATED_ONLY_ROUTES


def hash_password(password: str) -> str:
    """Hashear una contraseña con bcrypt y devolver string."""
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def compare_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    """Verificar y decodificar un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Validar que el token tenga user_id
        if "user_id" not in payload:
            raise HTTPException(status_code=401, detail="Token inválido: falta user_id")
        return payload
    except jwt.ExpiredSignatureError as e:
        print("verify_jwt_token - ExpiredSignatureError:", e)
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        print("verify_jwt_token - InvalidTokenError:", e)
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        print("verify_jwt_token - Exception:", repr(e))
        raise HTTPException(status_code=401, detail="Error de autenticación")


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware de autenticación y autorización unificado"""

    def __init__(self, app):
        super().__init__(app)
        self._permission_service = None

    def get_permission_service(self):
        """Obtener servicio de permisos con lazy loading"""
        if self._permission_service:
            return self._permission_service
        try:
            from config.cnx import SessionLocal
            from permisos.services import PermisoService
            db = SessionLocal()
            self._permission_service = PermisoService(db)
            return self._permission_service
        except Exception as e:
            print(f"Error creating permission service: {e}")
            return None

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Verificar prefijos públicos
        for prefix in PUBLIC_PATH_PREFIXES:
            if path.startswith(prefix):
                return await call_next(request)

        # Rutas totalmente públicas
        if path in PUBLIC_ROUTES:
            return await call_next(request)

        method = request.method

        # Permitir siempre OPTIONS para CORS
        if method == "OPTIONS":
            return await call_next(request)

        # Verificar rutas públicas con lógica
        if self.is_public_route(path, method):
            return await call_next(request)

        # Obtener el token del header Authorization
        authorization: Optional[str] = request.headers.get("Authorization")
        print("AuthMiddleware - Authorization header:", authorization)

        if not authorization:
            print("AuthMiddleware - no Authorization header present")
            # Devolver JSONResponse para que CORS pueda añadir cabeceras correctamente
            return JSONResponse(status_code=401, content={"detail": "Token de autorización requerido"})

        try:
            parts = authorization.split()
            if len(parts) != 2:
                return JSONResponse(status_code=401, content={"detail": "Formato de Authorization inválido"})
            scheme, token = parts
            if scheme.lower() != "bearer":
                return JSONResponse(status_code=401, content={"detail": "Esquema de autorización inválido. Use 'Bearer <token>'"})

            try:
                payload = verify_jwt_token(token)
            except HTTPException as ve:
                # Devolver respuesta directamente para que CORS la procese (no relanzar)
                return JSONResponse(status_code=ve.status_code, content={"detail": ve.detail})

            request.state.user = payload

            if self.should_check_permissions(path):
                user_role_id = payload.get('rol_id')
                if user_role_id:
                    normalized_path = self.normalize_path_for_permissions(path)
                    try:
                        service = self.get_permission_service()
                        if service:
                            has_permission = service.user_has_permission(user_role_id, normalized_path, method)
                            if not has_permission:
                                return JSONResponse(status_code=403, content={"detail": "No tiene permisos para acceder a este recurso"})
                        else:
                            print("Warning: Permission service not available, allowing access")
                    except Exception as permission_error:
                        print(f"Error verificando permisos: {permission_error}")

        except ValueError:
            return JSONResponse(status_code=401, content={"detail": "Formato de token inválido"})
        except Exception as e:
            print("AuthMiddleware unexpected error:", repr(e))
            return JSONResponse(status_code=401, content={"detail": "Error de autenticación"})

        return await call_next(request)

    def is_public_route(self, path: str, method: str) -> bool:
        """Verificar si una ruta es pública"""
        # Verificar rutas con métodos específicos
        if path in PUBLIC_METHODS and method in PUBLIC_METHODS[path]:
            return True

        # Permitir ver productos individuales sin autenticación
        import re
        if method == "GET" and re.match(r'^/productos/\d+$', path):
            return True
        if method == "GET" and re.match(r'^/cart_items/user/\d+$', path):
            return True

        # Prefijos ya cubiertos por dispatch, pero añadir caché de seguridad
        for public_prefix in ["/docs", "/redoc"]:
            if path.startswith(public_prefix):
                return True

        return False

    def should_check_permissions(self, path: str) -> bool:
        """Determinar si se debe verificar permisos para una ruta"""
        skip_permission_paths = ["/health", "/favicon.ico", "/openapi.json", "/docs", "/redoc"]
        for skip_path in skip_permission_paths:
            if path.startswith(skip_path):
                return False
        if path in AUTHENTICATED_ONLY_ROUTES:
            return False
        return True

    def normalize_path_for_permissions(self, path: str) -> str:
        """Normalizar ruta para verificación de permisos"""
        import re
        patterns = [
            (r'/usuarios/\d+', '/usuarios/{id}'),
            (r'/roles/\d+', '/roles/{id}'),
            (r'/productos/\d+', '/productos/{id}'),
            (r'/cart_items/\d+', '/cart_items/{id}'),
            (r'/cart_items/user/\d+', '/cart_items/user/{id}'),
            (r'/cart_items/user/\d+/clear', '/cart_items/user/{id}/clear'),
            (r'/permisos/\d+', '/permisos/{id}'),
            (r'/permisos/rol/\d+', '/permisos/rol/{id}'),
            (r'/permisos/usuario/\d+/permisos', '/permisos/usuario/{id}/permisos'),
            (r'/permisos/ruta/[^/]+/metodo/[^/]+', '/permisos/ruta/{ruta}/metodo/{metodo}'),
        ]
        normalized_path = path
        for pattern, replacement in patterns:
            normalized_path = re.sub(pattern, replacement, normalized_path)
        return normalized_path


### REVISAR 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency para verificar el token JWT en endpoints específicos
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Aquí podrías realizar validaciones adicionales si lo necesitas
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Dependency para obtener el usuario actual desde el middleware
async def get_current_user(request: Request):
    """Obtener el usuario actual desde el estado del request (middleware)"""
    if hasattr(request.state, 'user'):
        return request.state.user
    raise HTTPException(status_code=401, detail="Usuario no autenticado")