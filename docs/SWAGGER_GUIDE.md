# 🚀 Guía de Uso con Swagger UI - Kick Shopping API

Esta guía te explica cómo usar la **documentación interactiva Swagger** de la API de Kick Shopping.

## 🎯 Acceso Rápido

**URL de Swagger**: <http://localhost:5000/docs>

> **Nota**: Asegúrate de que el servidor esté corriendo antes de acceder a Swagger UI.

## 🔐 Autenticación en Swagger

### Paso 1: Hacer Login

1. **Encuentra el endpoint de login**:
   - Busca la sección **"Usuarios"**
   - Localiza `POST /usuarios/login`

2. **Probar el login**:
   - Click en `POST /usuarios/login`
   - Click en **"Try it out"**
   - En el campo Request body, usa:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
   - Click en **"Execute"**

3. **Copiar el token**:
   - En la respuesta, copia el valor del campo `token`
   - Debería verse así: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...`

### Paso 2: Configurar Autorización

1. **Buscar el botón Authorize**:
   - En la esquina superior derecha de Swagger UI
   - Click en el botón **"Authorize"** 🔒

2. **Configurar Bearer Token**:
   - Se abrirá un modal de autorización
   - En el campo **"Value"** pega tu token
   - **NO** agregues "Bearer " al inicio, solo pega el token
   - Click en **"Authorize"**
   - Click en **"Close"**

3. **¡Listo!**:
   - Ahora verás un candado cerrado 🔒 en los endpoints protegidos
   - Todos los requests incluirán automáticamente tu token

## 👥 Usuarios de Prueba

| Usuario     | Contraseña  | Rol           | Permisos                    |
| ----------- | ----------- | ------------- | --------------------------- |
| admin       | admin123    | Administrador | ✅ Acceso completo         |
| gerente01   | gerente123  | Gerente       | ✅ Gestión y supervisión   |
| empleado01  | empleado123 | Empleado      | ⚠️ Acceso limitado         |

## 📋 Navegación por Módulos

### 🏠 Default
- Información básica del sistema
- Health check

### 👥 Usuarios
- **`POST /usuarios/login`** - 🟢 Público - Login del sistema
- **`GET /usuarios`** - 🔒 Protegido - Listar usuarios
- **`GET /usuarios/me`** - 🔒 Protegido - Mi perfil
- **`POST /usuarios`** - 🔒 Protegido - Crear usuario
- **`PUT /usuarios/{id}`** - 🔒 Protegido - Actualizar usuario
- **`DELETE /usuarios/{id}`** - 🔒 Protegido - Eliminar usuario

### 🛡️ Roles
- **`GET /roles`** - 🔒 Protegido - Listar roles
- **`POST /roles`** - 🔒 Protegido - Crear rol
- **`PUT /roles/{id}`** - 🔒 Protegido - Actualizar rol
- **`DELETE /roles/{id}`** - 🔒 Protegido - Eliminar rol

### 🔐 Permisos (Nuevo!)
- **`GET /permisos`** - 🔒 Protegido - Listar permisos
- **`POST /permisos`** - 🔒 Protegido - Crear permiso
- **`GET /permisos/{id}`** - 🔒 Protegido - Obtener permiso
- **`PUT /permisos/{id}`** - 🔒 Protegido - Actualizar permiso
- **`DELETE /permisos/{id}`** - 🔒 Protegido - Eliminar permiso

#### Gestión Avanzada de Permisos:
- **`POST /permisos/rol/assign`** - Asignar permisos a rol
- **`POST /permisos/rol/remove`** - Remover permisos de rol
- **`GET /permisos/rol/{rol_id}`** - Ver permisos de un rol
- **`GET /permisos/usuario/{user_rol_id}/permisos`** - Permisos de usuario
- **`POST /permisos/usuario/verify`** - Verificar permiso específico

### 📦 Productos, 📂 Categorías, 🪑 Mesas, 💰 Ventas, etc.
- Todos siguen el mismo patrón CRUD
- Requieren autenticación
- Algunos requieren permisos específicos según el rol

## 🎯 Ejemplos Prácticos

### 1. Primer Login y Exploración

1. **Login** con `admin/admin123`
2. **Autorizar** en Swagger con el token obtenido
3. **Probar** `GET /usuarios/me` para ver tu perfil
4. **Explorar** `GET /usuarios` para ver todos los usuarios

### 2. Gestión de Permisos

1. **Ver permisos disponibles**: `GET /permisos`
2. **Ver permisos de tu rol**: `GET /permisos/rol/1`
3. **Verificar un permiso específico**: `POST /permisos/usuario/verify`

### 3. CRUD Básico de Productos

1. **Listar productos**: `GET /productos`
2. **Crear producto nuevo**: `POST /productos`
3. **Actualizar producto**: `PUT /productos/{id}`
4. **Eliminar producto**: `DELETE /productos/{id}`

## 🔄 Refrescar Token

Si tu sesión expira (después de 30 minutos):

1. **Repetir el proceso de login**
2. **Actualizar la autorización** con el nuevo token
3. **Continuar usando la API**

## 💡 Tips y Trucos

### ✅ Buenas Prácticas
- **Usar admin** para probar todas las funcionalidades
- **Copiar ejemplos** de Request/Response para entender la estructura
- **Leer las descripciones** de cada endpoint
- **Probar con diferentes roles** para entender el sistema de permisos

### ⚠️ Errores Comunes
- **Token no configurado**: Error 401 - Configurar autorización
- **Permisos insuficientes**: Error 403 - Usar usuario con más permisos  
- **Token expirado**: Error 401 - Hacer login nuevamente
- **Datos inválidos**: Error 422 - Revisar el formato del Request Body

### 🚀 Funcionalidades Avanzadas
- **Filtros y paginación**: Disponibles en endpoints de listado
- **Búsqueda específica**: Algunos endpoints permiten filtros
- **Responses detallados**: Incluyen códigos de error específicos
- **Validación automática**: Swagger valida los datos antes de enviar

## 📊 Códigos de Respuesta

| Código | Significado | Cuándo Aparece |
| ------ | ----------- | -------------- |
| 200    | ✅ OK | Operación exitosa |
| 201    | ✅ Creado | Recurso creado exitosamente |
| 400    | ❌ Bad Request | Datos inválidos en el request |
| 401    | 🔒 Unauthorized | Token inválido o faltante |
| 403    | 🚫 Forbidden | Sin permisos para el recurso |
| 404    | 🔍 Not Found | Recurso no encontrado |
| 422    | ⚠️ Validation Error | Error de validación de datos |
| 500    | 💥 Server Error | Error interno del servidor |

## 🔗 Recursos Adicionales

- **Documentación Completa**: [`README.md`](./README.md)
- **Guía de Postman**: [`POSTMAN_GUIDE.md`](./POSTMAN_GUIDE.md)  
- **Referencia de API**: [`API_REFERENCE.md`](./API_REFERENCE.md)
- **Guía de Seguridad**: [`SECURITY_GUIDE.md`](./SECURITY_GUIDE.md)

---

**🎉 ¡Swagger UI te permite probar toda la API sin escribir código!**

> **Próximos pasos**: Una vez que domines Swagger, puedes usar la [Guía de Postman](./POSTMAN_GUIDE.md) para automatizar tests y crear collections reutilizables.