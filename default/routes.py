from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from uuid import uuid4
import os

default = APIRouter()

@default.get("/")
@default.get("/home")
def index():
    """Endpoint de inicio"""
    try:
        return {
            "message": f"Hola FAST API",
            "status": "running",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado en el endpoint de inicio"
        )

@default.get("/test")
def test():
    """Endpoint de prueba"""
    try:
        resp = {
            'firstName': 'Daniel',
            'lastName': 'Cazabat',
            'age': 55,
            'city': 'San Carlos de Bolivar',
            'timestamp': str(datetime.now())
        }
        return resp
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado en el endpoint de prueba"
        )

@default.get("/health")
def health_check():
    """Endpoint de health check"""
    try:
        return {
            "status": "healthy",
            "timestamp": str(datetime.now()),
            "request_id": str(uuid4()),
            "service": "FastAPI Users & Tasks API"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error en el health check"
        )

# Ruta para servir favicon.ico y evitar error en Swagger UI
@default.get('/favicon.ico', include_in_schema=False)
async def favicon():
    """Servir favicon"""
    try:
        favicon_path = 'favicon.svg'
        if os.path.exists(favicon_path):
            return FileResponse(favicon_path)
        else:
            # Si no existe el archivo, devolver un 404
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favicon no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al servir el favicon"
        )


# DEBUG endpoint (temporal) para inspeccionar la cadena de conexión y archivo sqlite
@default.get('/debug/dbinfo', include_in_schema=False)
def debug_dbinfo():
    try:
        from config import STRCNX
        import os
        info = {
            'STRCNX': STRCNX,
            'db_file_exists': False,
            'db_file_path': None
        }
        # si es sqlite, obtener ruta del archivo
        if STRCNX and STRCNX.startswith('sqlite'):
            # quitar prefijo sqlite:/// o sqlite://// según venga
            path = STRCNX.split('///', 1)[-1]
            # Normalizar ruta relativa a cwd si no es absoluta
            if not (path.startswith('/') or (len(path) > 1 and path[1] == ':')):
                path = os.path.join(os.getcwd(), path)
            info['db_file_path'] = path
            info['db_file_exists'] = os.path.exists(path)
        return info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))