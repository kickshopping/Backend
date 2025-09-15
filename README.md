# KickShopping Backend

Backend en FastAPI para la tienda KickShopping.

##  Pasos para usar el proyecto


1. **Activa el entorno virtual** (si no está activo):
   ```powershell
   .\venv\Scripts\activate
   ```


2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```


3. **Ejecuta las migraciones Alembic:**
   ```bash
   alembic upgrade head
   ```


4. **Inserta productos de prueba:**
   ```powershell
   python -m cart.seed_products



5. **Inicia el servidor FastAPI:**
   ```bash
   uvicorn config.app:app --reload
   ```


6. **Prueba los endpoints en el navegador:**
   - Abre [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver la documentación interactiva (Swagger).
   - Desde Swagger puedes:
     - Ver todos los endpoints disponibles y sus descripciones.
     - Probar cada endpoint (crear productos, agregar al carrito, ver, remover y vaciar) usando los formularios web.
     - Ver ejemplos de datos y respuestas.


7. **Ejecuta los tests automáticos:**
   ```bash
   pytest tests/test_cart.py
   ```

## 📦 Estructura principal

- `cart/`: Lógica de carrito y productos
- `config/`: Configuración de base de datos y modelos
- `tests/`: Pruebas automáticas
- `alembic/`: Migraciones de base de datos

## 🛒 Endpoints principales y ejemplos

### 1. Crear producto
**POST** `/cart/products`

Body (JSON):
```json
{
   "nombre": "Zapatillas Nike Air",
   "descripcion": "Zapatillas deportivas",
   "precio": 120.0
}
```

### 2. Agregar producto al carrito
**POST** `/cart/{user_id}/add`
Ejemplo: `/cart/usuario1/add`

Body (JSON):
```json
{
   "product_id": 1,
   "cantidad": 2
}
```

### 3. Ver carrito y total
**GET** `/cart/{user_id}`
Ejemplo: `/cart/usuario1`

### 4. Remover producto del carrito
**DELETE** `/cart/{user_id}/remove/{product_id}`
Ejemplo: `/cart/usuario1/remove/1`

### 5. Vaciar carrito
**DELETE** `/cart/{user_id}/clear`
Ejemplo: `/cart/usuario1/clear`

---
