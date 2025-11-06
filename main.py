"""
KickShopping API - Aplicación Principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

# Configuración de base de datos y modelos
from config.database_session import engine
from config.basemodel import Base

# Importar modelos para crear tablas
from permisos.model import Permiso  # Importar primero para evitar errores de dependencias circulares
from roles.model import Rol
from usuarios.model import Usuario
from productos.model import Product
from cart_items.model import CartItem
from config.associations import rol_permiso_association

# Importar rutas
from default.routes import default
from roles.routes import roles
from usuarios.routes import usuarios
from productos.routes import products
from cart_items.routes import cart_items
from permisos.routes import router as permisos_router
from middlewares.auth import AuthMiddleware

def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI
    """
    app = FastAPI(
        title="Kick Shopping API",
        description="API para gestionar una tienda de Indumentaria",
        version="1.0"
    )

    # Configuración de orígenes permitidos para CORS
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ]

    # Agregar middleware de autenticación primero
    app.add_middleware(AuthMiddleware)

    # Agregar middleware CORS después para que pueda manejar las respuestas de auth
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With"
        ],
        expose_headers=["Authorization"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )

    # Registrar rutas
    app.include_router(default, prefix="", tags=["Default"])
    app.include_router(roles, prefix="/roles", tags=["Roles"])
    app.include_router(usuarios, prefix="/usuarios", tags=["Usuarios"])
    app.include_router(products, prefix="/productos", tags=["Productos"])
    app.include_router(cart_items, prefix="/cart_items", tags=["Carrito"])
    app.include_router(permisos_router, prefix="/permisos", tags=["Permisos"])

    # Servir archivos estáticos (imágenes subidas)
    # Montamos la carpeta ./static en /static para que las imágenes estén accesibles
    app.mount("/static", StaticFiles(directory="static"), name="static")

    return app

# Crear tablas e inicializar aplicación
create_tables()
app = get_application()

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
