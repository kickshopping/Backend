from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cart.routes.cart_routes import router as cart_router
from config.basemodel import Base
from config.cnx import engine

app = FastAPI(
    title="KickShopping",
    description="API para la gestión de carrito de compras en KickShopping",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raíz para verificar funcionamiento
@app.get("/")
def index():
    """Endpoint raíz que retorna un mensaje de bienvenida."""
    return {"Hola": "FastAPI"}

# Incluye las rutas del carrito bajo el prefijo /cart y el tag "Carrito"
app.include_router(cart_router, prefix="/cart", tags=["Carrito"])

# Crea todas las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)


