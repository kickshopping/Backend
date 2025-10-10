from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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


# Asignamos los Middleware para los CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=['*'],
    allow_credentials=True,
)
# Agregamos el middleware de autenticación
app.add_middleware(AuthMiddleware)

#Routas de la API
app.include_router(default, prefix='', tags=['Rutas por Default'])

app.include_router(roles, prefix="/roles", tags=["Roles"])
app.include_router(usuarios, prefix="/usuarios", tags=["Usuarios"])
app.include_router(products, prefix="/productos", tags=["Productos"])
app.include_router(cart_items, prefix="/cart_items", tags=["Carrito"])
app.include_router(permisos_router, prefix="/permisos", tags=["Permisos"])

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
