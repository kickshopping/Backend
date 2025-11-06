<<<<<<< HEAD

# KickShopping Backend

Backend en FastAPI para la tienda KickShopping.

## Pasos para usar el proyecto

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



   ```
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

```markdown
# KickShopping (monorepo)

Este repositorio contiene el backend (FastAPI) y el frontend (Next.js/React) de la tienda KickShopping.

Este README describe cómo levantar ambos servicios en desarrollo, la estructura principal y notas útiles para desarrollar y depurar (autenticación, subida de imágenes, categorías, etc.).

---

## Estructura del repositorio (resumen)

- `backend-kikshopping/` — Backend en FastAPI (Python + SQLAlchemy).
- `frontend-kikshopping/` — Frontend en Next.js (React + TypeScript).
- `nombre_del_entorno/` — (opcional) entorno virtual local mostrado en el workspace.

Cada subcarpeta contiene su propio README y comandos de inicio. A continuación se explica cómo trabajar con ambos.

---

## Backend — `backend-kikshopping`

Descripción rápida: API REST en FastAPI que expone endpoints para usuarios, roles/permisos, productos y carrito. Soporta autenticación JWT (access + refresh) y cuenta con seeders para datos de prueba.

Rutas clave (resumen):

- `POST /usuarios/login` — Login y obtención de token (access & refresh).
- `GET /usuarios/me` — Obtener perfil del usuario.
- `GET /productos` — Listar productos.
- `GET /productos/{id}` — Detalle de producto.
- `POST /productos/upload` — Subir imagen y crear producto (multipart/form-data).
- `POST /productos/{product_id}/imagen` — Actualizar la imagen de un producto (requiere rol admin).
- `PATCH /productos/{product_id}` — Actualizar campos del producto (requiere admin).
- `GET /categoria/{category}` — Listar productos por categoría.
- `POST/GET/PATCH /cart_items` — Endpoints de carrito.

Notas importantes del backend:

- La subida de imágenes guarda el fichero en `static/uploads/` y devuelve `image_url` del tipo `/static/uploads/<filename>`.
- Cuando se actualiza la imagen de un producto, el backend ahora intenta eliminar el archivo anterior del directorio `static/uploads/` para evitar archivos huérfanos (siempre de forma segura y no bloqueante).
- Las rutas de creación/edición de productos y la subida de imágenes usan la dependencia `verify_admin` y por tanto requieren un token válido con permisos de administrador.

Instalación y ejecución (Windows / PowerShell):

```powershell
# entrar al backend
cd backend-kikshopping

# crear/activar entorno virtual (si no lo tienes)
python -m venv .venv
& .venv\Scripts\Activate.ps1

# instalar dependencias
pip install -r requirements.txt

# ejecutar migraciones (si usas alembic)
alembic upgrade head

# ejecutar seeders (opcional)
python ./seeders/seed_main.py

# iniciar servidor en desarrollo
uvicorn config.app:app --reload --host 0.0.0.0 --port 8000

# abrir docs: http://localhost:8000/docs
```

Logs y debugging:

- Revisa la consola donde corre `uvicorn` para ver errores del servidor.
- Si obtienes errores 401/403 en subida de imagen, revisa que el usuario tenga rol de administrador (usar `/usuarios/login` para obtener token y probar en Swagger o Postman).

---

## Frontend — `frontend-kikshopping`

Descripción rápida: aplicación Next.js que consume la API del backend. Contiene páginas para listar productos, ver detalles, publicar y editar productos, y un carrito.

Puntos relevantes implementados en este repo:

- Páginas con formulario de edición y creación de producto:
  - `app/editar-producto/page.tsx` — Editar producto: permite cambiar imagen, título, precio, descripción, categoría y descuento. Ahora usa `authFetch` para subir la imagen y el PATCH (manejo de refresh de token).
  - `app/publicar-producto/page.tsx` — Publicar nuevo producto: incluye subida de imagen (FormData), descuento, descripción y selección de sección/categoría.
- Client-side image processing:
  - Ambas páginas usan redimensionado en cliente (canvas) para ajustar imágenes grandes y mantener transparencia en PNG cuando es posible.
  - En edición, si la subida inicial falla con 403 se reintenta automáticamente convirtiendo la imagen a JPEG (fallback) para mejorar compatibilidad con ciertos backends.
- Autenticación y tokens:
  - El token se guarda en `localStorage` bajo la clave `tokenkick` y hay un `authFetch` en `lib/api.ts` que maneja refresh automático mediante el endpoint `/usuarios/refresh`.
- Menú y categorías:
  - El menú principal se encuentra en `app/components/Header.tsx`. Se añadió la categoría `buzos-mujer` al menú para mantener consistencia.

Instalación y ejecución (Windows / PowerShell):

```powershell
cd frontend-kikshopping
# instalar dependencias (usa npm o pnpm segun prefieras)
npm install

# iniciar el servidor de desarrollo
npm run dev

# por defecto Next escucha en http://localhost:3000
```

Notas de configuración:

- Asegúrate de que la variable `NEXT_PUBLIC_API_URL` apunte al backend (ej: `http://localhost:8000`). Puedes definirla en `.env.local` en la carpeta del frontend:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Flujos comunes y debugging (resumen rápido)

- Problema: 403 al subir imagen desde la UI de editar producto
  - Causas comunes: token no válido / usuario sin rol admin; backend valida tipo de archivo; CORS
  - Qué hice en el repo: el frontend ahora usa `authFetch` (intenta refresh de token) y reintenta con conversión a JPEG si recibe 403; el backend intenta eliminar imagen antigua tras actualizar la ruta.

- Si el error persiste:
  1. Abre las devtools del navegador y revisa la petición POST a `/productos/{id}/imagen` — mira `Request Headers` y `Response body`.
  2. Revisa los logs del servidor (uvicorn) para ver la traza en backend.
  3. Verifica que el usuario con el que estás logueado tiene rol admin (usar `/usuarios/login` y comprobar `user_type` en el token o en `localStorage`).

---

## Comandos útiles

- Backend (desde `backend-kikshopping`):
  - Crear/activar venv, instalar dependencias, correr `uvicorn` y migraciones (ver arriba).

- Frontend (desde `frontend-kikshopping`):
  - `npm install`
  - `npm run dev`

---

## Desarrollo y contribuciones

- El proyecto está organizado por módulos (cada carpeta con sus modelos, DTOs, servicios y rutas) para facilitar la extensión y pruebas unitarias.
- Para contribuir: crea una rama por feature, añade pruebas cuando corresponda y abre PR describiendo el cambio.

---

Si quieres que deje este README más específico (por ejemplo, añadir ejemplos de payloads exactos para upload, o instrucciones para Docker), dime qué prefieres y lo actualizo.

``` 
- ✅ Tokens JWT con expiración configurable (30 minutos por defecto)
