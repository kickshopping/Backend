from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import logging
import os

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
from config.basemodel import Base
from config.cnx import engine

# Importar todos los modelos para asegurar que se registren en Base.metadata
from roles.model import Rol
from permisos.model import Permiso
from usuarios.model import Usuario
from productos.model import Product
from cart_items.model import CartItem
from config.associations import rol_permiso_association

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Importamos las rutas de los diferentes modelos 
from default.routes import default
from middlewares.auth import AuthMiddleware
from roles.routes import roles
from usuarios.routes import usuarios
from productos.routes import products
from cart_items.routes import cart_items
from permisos.routes import router as permisos_router

app = FastAPI(
    title="Kick Shopping API",
    description="Esta es la API para gestionar una tienda de Indumentaria",
    version="1.0"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Request headers: {request.headers}")
        
        response = await call_next(request)
        
        logger.info(f"Response status: {response.status_code}")
        if response.status_code >= 400:
            logger.warning(f"Error response: {response.status_code}")
        
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise


# Asignamos los Middleware para los CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=3600,  # Cache preflight requests for 1 hour
)
# Configurar archivos estáticos
static_dir = "static"
uploads_dir = os.path.join(static_dir, "uploads")

# Asegurar que los directorios existen
if not os.path.exists(static_dir):
    logger.info(f"Creating static directory: {static_dir}")
    os.makedirs(static_dir)
if not os.path.exists(uploads_dir):
    logger.info(f"Creating uploads directory: {uploads_dir}")
    os.makedirs(uploads_dir)

logger.info(f"Mounting static files from: {static_dir}")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Rutas de la API
app.include_router(default, prefix='', tags=['Rutas por Default'])

app.include_router(roles, prefix="/roles", tags=["Roles"])
app.include_router(usuarios, prefix="/usuarios", tags=["Usuarios"])
app.include_router(products, prefix="/productos", tags=["Productos"])
app.include_router(cart_items, prefix="/cart_items", tags=["Carrito"])
app.include_router(permisos_router, prefix="/permisos", tags=["Permisos"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="127.0.0.1",
        port=8000,
        timeout_keep_alive=65,  # Aumentar el timeout de keep-alive
        log_level="info",
        reload=True  # Habilitar hot-reload para desarrollo
    )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Kick Shopping API",
        version="1.0",
        description="Esta es la API para gestionar una tienda de calzado deportivo",
        routes=app.routes,
    )
    
    # Configurar el esquema de seguridad personalizado - ESTO ES CLAVE
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
