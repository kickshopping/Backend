# 📋 API Reference - Kick Shopping Backend

## 🚀 Base URL
```
http://localhost:5000
```

## 🔐 Autenticación

### Login (Público)
```http
POST /usuarios/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "username": "admin"
}
```

### Usar Token en Requests
```http
Authorization: Bearer <token>
```

## 📋 Endpoints por Módulo

### 👥 Usuarios (`/usuarios`)
```http
GET    /usuarios              # Listar usuarios (requiere auth)
GET    /usuarios/me           # Obtener perfil actual (requiere auth) 
GET    /usuarios/{id}         # Obtener usuario por ID (requiere auth)
POST   /usuarios              # Crear usuario (requiere auth + permisos)
POST   /usuarios/login        # Login (público)
PUT    /usuarios/{id}         # Actualizar usuario (requiere auth + permisos)
DELETE /usuarios/{id}         # Eliminar usuario (requiere auth + permisos)
```

### 🛡️ Roles (`/roles`)
```http
GET    /roles                 # Listar roles (requiere auth)
GET    /roles/{id}            # Obtener rol por ID (requiere auth)  
POST   /roles                 # Crear rol (requiere auth + permisos)
PUT    /roles/{id}            # Actualizar rol (requiere auth + permisos)
DELETE /roles/{id}            # Eliminar rol (requiere auth + permisos)
```

### 🔐 Permisos (`/permisos`)
```http
GET    /permisos                                    # Listar permisos
GET    /permisos/{id}                               # Obtener permiso por ID
GET    /permisos/ruta/{ruta}/metodo/{metodo}        # Buscar por ruta y método
POST   /permisos                                    # Crear permiso
PUT    /permisos/{id}                               # Actualizar permiso  
DELETE /permisos/{id}                               # Eliminar permiso

# Gestión Rol-Permiso
POST   /permisos/rol/assign                         # Asignar permisos a rol
POST   /permisos/rol/remove                         # Remover permisos de rol
GET    /permisos/rol/{rol_id}                       # Ver permisos de un rol

# Verificación de Permisos
GET    /permisos/usuario/{user_rol_id}/permisos     # Permisos de usuario
POST   /permisos/usuario/verify                     # Verificar permiso específico
```

### � Productos (`/productos`)
```http
GET    /productos         # Listar productos de calzado (requiere auth)
GET    /productos/{id}    # Obtener producto por ID (requiere auth)
POST   /productos         # Crear producto (requiere auth + permisos)
PATCH  /productos/{id}    # Actualizar producto (requiere auth + permisos)
DELETE /productos/{id}    # Eliminar producto (requiere auth + permisos)
```

### � Carrito (`/cart_items`)
```http
GET    /cart_items                    # Listar todos los elementos del carrito (requiere auth)
GET    /cart_items/user/{id}          # Obtener carrito de un usuario (requiere auth)
GET    /cart_items/{id}               # Obtener elemento del carrito por ID (requiere auth)
POST   /cart_items                    # Agregar elemento al carrito (requiere auth)
PATCH  /cart_items/{id}               # Actualizar elemento del carrito (requiere auth)
DELETE /cart_items/{id}               # Eliminar elemento del carrito (requiere auth)
DELETE /cart_items/user/{id}/clear    # Limpiar carrito de un usuario (requiere auth)
```



## 🚫 Endpoints Públicos (Sin Autenticación)

```
GET    /                  # Página principal
GET    /docs              # Documentación Swagger UI
GET    /redoc             # Documentación ReDoc
GET    /openapi.json      # Especificación OpenAPI
GET    /health            # Health check
POST   /usuarios          # Registro de nuevos usuarios
POST   /usuarios/login    # Login de usuarios
```

## 🔒 Flujo de Autenticación

1. **Registro**: `POST /usuarios` con datos del usuario
2. **Login**: `POST /usuarios/login` con username/password
3. **Uso**: Incluir token en header: `Authorization: Bearer <token>`

## 📝 Formato de Respuestas

### Éxito (200/201)
```json
{
  "data": { /* objeto o array */ },
  "message": "Operación exitosa"
}
```

### Error (400/401/403/404/500)
```json
{
  "detail": "Descripción del error"
}
```

## 🧪 Ejemplos de Uso con curl

### Login
```bash
curl -X POST "http://localhost:8000/usuarios/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password123"
```

### Consultar datos protegidos
```bash
curl -X GET "http://localhost:8000/productos" \
  -H "Authorization: Bearer <tu-token-aqui>"
```

### Crear producto
```bash
curl -X POST "http://localhost:8000/productos" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu-token-aqui>" \
  -d '{"pro_nombre":"Café Americano","pro_cat_id":1,"pro_cantidad_stock":50}'
```