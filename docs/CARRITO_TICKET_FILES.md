# Archivos relacionados con Carrito y Ticket

A continuación tienes la lista de archivos que se agregaron o modificaron en la implementación del carrito y la generación/envío del ticket, con su ruta y una breve descripción.

## Backend

- `backend-kikshopping/cart_items/purchase_service.py`
  - Genera el ticket de compra a partir de los items del carrito del usuario, calcula totales, borra los items del carrito, intenta enviar el email y devuelve el ticket (dict).

- `backend-kikshopping/cart_items/purchase.py`
  - Modelos Pydantic para la respuesta del ticket: `PurchaseItemOut` y `PurchaseTicket`.

- `backend-kikshopping/cart_items/email.py`
  - Formatea el ticket en HTML/plain y envía el correo vía SMTP (`send_purchase_ticket_email`). Maneja errores de envío sin romper la compra.

- `backend-kikshopping/cart_items/routes.py`
  - Endpoint POST `/cart_items/purchase` que valida autenticación y llama a `generate_purchase_ticket`.
  - Contiene la API REST del carrito (GET/POST/PATCH/DELETE/increment/decrement).

- `backend-kikshopping/config/email.py`
  - Variables de configuración para SMTP y destinatarios por defecto (`PURCHASE_EMAILS`).

- `backend-kikshopping/middlewares/cart_auth.py`
  - Dependencia `verify_token_and_permissions` usada por la ruta de `purchase` para validar token JWT (y permisos si se especifican).

- `backend-kikshopping/main.py`
  - Asegura inclusión del router `cart_items` (mencionado por completitud).

## Frontend

- `frontend-kikshopping/app/carrito/page.tsx`
  - Página del carrito (vista, incremento/decremento/eliminar items, `Finalizar Compra` que hace POST `/cart_items/purchase`).
  - Actualizados los enlaces del menú hamburguesa para que apunten a `/categoria/...` y `/productos`.

- `frontend-kikshopping/app/ticket/page.tsx`
  - Página que muestra el ticket: lee `localStorage.lastTicket` (guardado tras finalizar compra) y renderiza la tabla con items, totales y botones para imprimir / volver al inicio.

- `frontend-kikshopping/app/ticket/ticket.module.css`
  - Estilos para la página del ticket.

- `frontend-kikshopping/app/categoria/[category]/page.tsx`
  - Página de categoría: normaliza el slug recibido en la URL (quita sufijos `-hombre|-mujer|-unisex` y reemplaza guiones por espacios) antes de llamar al backend para obtener los productos.
  - Hace que al hacer click en un producto se vaya a la página detallada del producto.

- `frontend-kikshopping/app/productos/[id]/page.tsx`
  - Página detallada del producto en la ruta `/productos/[id]` (imagen grande, descripción, precio, descuento y botones para comprar/agregar al carrito). Basada en la implementación original `app/product/page.tsx`.

- `frontend-kikshopping/app/productos/[id]/product.module.css`
  - Estilos para la página detallada del producto (copiados/adaptados de `app/product/product.module.css`).

- `frontend-kikshopping/app/components/Navbar.tsx`
  - Navbar del sitio: se actualizaron los links del menú hamburguesa (antes `href="#"`) para apuntar a las rutas correctas de categorías.

- `frontend-kikshopping/app/product/page.tsx` (referencia)
  - Página de producto original que se usó como referencia para implementar la nueva ruta `/productos/[id]`.

## Notas adicionales

- Flujo de la compra:
  1. Frontend POST `/cart_items/purchase` con token.
  2. Backend genera ticket, limpia carrito, intenta enviar email y devuelve ticket.
  3. Frontend guarda ticket en `localStorage.lastTicket` y redirige a `/ticket`.

- Variables de entorno relevantes:
  - `NEXT_PUBLIC_API_URL` (frontend) — URL base del backend, ej. `http://localhost:8000`.
  - SMTP: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_USE_TLS`, `EMAIL_FROM`, `PURCHASE_EMAILS`.
