# Backend KickShopping (FastAPI)

## Instalación

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Crea las tablas de la base de datos:
   ```bash
   python -c "from app.utils import create_tables; create_tables()"
   ```

3. Ejecuta el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints principales
- `/auth/register` - Registro de usuario
- `/auth/login` - Login de usuario (OAuth2)
- `/products/` - Listado de productos
- `/products/{id}` - Detalle de producto
- `/cart/` - Carrito de usuario (GET, POST, DELETE)
- `/users/me` - Perfil de usuario (GET, PUT)
