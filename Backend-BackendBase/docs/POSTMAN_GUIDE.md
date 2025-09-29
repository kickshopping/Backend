# 📮 Guía de Uso con Postman - Kick Shopping API

Esta guía te explica cómo usar la API de Kick Shopping con **Postman** paso a paso.

## 🚀 Configuración Inicial

### 1. Información del Servidor

- **Base URL**: `http://localhost:5000`
- **Puerto**: 5000
- **Protocolo**: HTTP

### 2. Usuarios de Prueba

| Usuario    | Contraseña | Rol           |
| ---------- | ----------- | ------------- |
| admin      | admin123    | Administrador |
| gerente01  | gerente123  | Gerente       |
| empleado01 | empleado123 | Empleado      |

## 🔐 Proceso de Autenticación

### Paso 1: Hacer Login

**Request:**

```http
POST http://localhost:5000/usuarios/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta Esperada:**

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTU0MjQyMzB9.abc123...",
  "user_id": 1,
  "username": "admin"
}
```

### Paso 2: Configurar Authorization en Postman

#### Opción A: Usando Authorization Tab (Recomendado)

1. En cualquier request, ve a la tab **"Authorization"**
2. En "Type" selecciona **"Bearer Token"**
3. En "Token" pega el token obtenido del login
4. ¡Listo! Postman agregará automáticamente el header

#### Opción B: Usando Headers Manualmente

1. Ve a la tab **"Headers"**
2. Agrega un nuevo header:
   - **Key**: `Authorization`
   - **Value**: `Bearer tu-token-aqui`

### Paso 3: Variables de Entorno (Opcional pero Recomendado)

1. **Crear Environment**:

   - Click en "Environments" (ícono de ojo)
   - Click "Add"
   - Nombre: "Kick Shopping Local"
2. **Agregar Variables**:

   ```
   base_url: http://localhost:5000
   token: {{token}}
   user_id: {{user_id}}
   ```
3. **Usar en Requests**:

   - URL: `{{base_url}}/usuarios`
   - Authorization: `Bearer {{token}}`

## 📋 Ejemplos de Requests Comunes

### 1. Listar Usuarios

```http
GET {{base_url}}/usuarios
Authorization: Bearer {{token}}
```

### 2. Obtener Mi Perfil

```http
GET {{base_url}}/usuarios/me
Authorization: Bearer {{token}}
```

### 3. Crear Nuevo Usuario

```http
POST {{base_url}}/usuarios
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "password": "password123",
  "email": "usuario@ejemplo.com",
  "rol_id": 3
}
```

### 4. Listar Productos

```http
GET {{base_url}}/productos
Authorization: Bearer {{token}}
```

### 5. Crear Producto

```http
POST {{base_url}}/productos
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "producto_nombre": "Café Americano",
  "producto_descripcion": "Café negro tradicional",
  "producto_precio": 2500,
  "categoria_id": 1,
  "subcategoria_id": 1
}
```

### 6. Gestión de Permisos

#### Listar Permisos

```http
GET {{base_url}}/permisos
Authorization: Bearer {{token}}
```

#### Asignar Permisos a Rol

```http
POST {{base_url}}/permisos/rol/assign
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "rol_id": 2,
  "permiso_ids": [1, 2, 3, 4, 5]
}
```

#### Verificar Permisos de Usuario

```http
GET {{base_url}}/permisos/usuario/1/permisos
Authorization: Bearer {{token}}
```

## 🔄 Collection de Postman (Recomendado)

### Crear Collection Organizada

```json
{
  "info": {
    "name": "Kick Shopping API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{token}}",
        "type": "string"
      }
    ]
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000"
    }
  ]
}
```

### Estructura de Carpetas Sugerida:

```
📁 Kick Shopping API/
├── 🔐 Auth/
│   └── Login
├── 👥 Usuarios/
│   ├── Listar Usuarios
│   ├── Mi Perfil
│   ├── Crear Usuario
│   └── Actualizar Usuario
├── 🛡️ Roles/
│   ├── Listar Roles
│   └── Crear Rol
├── 🔐 Permisos/
│   ├── Listar Permisos
│   ├── Asignar a Rol
│   └── Verificar Usuario
├── 📦 Productos/
├── 📂 Categorías/
├── 🪑 Mesas/
└── 💰 Ventas/
```

## ⚠️ Errores Comunes y Soluciones

### 1. Token Expirado

**Error:** `HTTP 401 - Token has expired`
**Solución:** Hacer login nuevamente y actualizar el token

### 2. Permisos Insuficientes

**Error:** `HTTP 403 - No tienes permisos para acceder a este recurso`
**Solución:** Usar un usuario con permisos apropiados (admin, gerente)

### 3. Token Mal Formateado

**Error:** `HTTP 401 - Could not validate credentials`
**Solución:** Verificar que el header sea: `Authorization: Bearer token_aqui`

### 4. Servidor No Disponible

**Error:** `Could not get response`
**Solución:** Verificar que el servidor esté corriendo en puerto 5000

## 🧪 Scripts de Postman (Avanzado)

### Pre-request Script para Auto-login

```javascript
// Si no hay token o está expirado, hacer login automático
if (!pm.environment.get("token") || isTokenExpired()) {
    const loginRequest = {
        url: pm.environment.get("base_url") + "/usuarios/login",
        method: 'POST',
        header: {
            'Content-Type': 'application/json',
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                username: "admin",
                password: "admin123"
            })
        }
    };
  
    pm.sendRequest(loginRequest, (err, res) => {
        if (err) {
            console.log(err);
        } else {
            const responseJson = res.json();
            pm.environment.set("token", responseJson.token);
            pm.environment.set("user_id", responseJson.user_id);
        }
    });
}

function isTokenExpired() {
    // Lógica simple para verificar expiración
    // En producción deberías decodificar el JWT
    return false;
}
```

### Test Script para Guardar Token

```javascript
// Guardar token automáticamente después del login
if (responseCode.code === 200) {
    const jsonData = pm.response.json();
  
    if (jsonData.token) {
        pm.environment.set("token", jsonData.token);
        pm.environment.set("user_id", jsonData.user_id);
        pm.environment.set("username", jsonData.username);
      
        console.log("Token guardado exitosamente");
    }
}
```

## 📊 Monitoring y Testing

### Tests Básicos en Postman

```javascript
// Verificar status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Verificar tiempo de respuesta
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

// Verificar estructura de respuesta
pm.test("Response has required fields", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('token');
    pm.expect(jsonData).to.have.property('user_id');
});
```

---

**🎉 ¡Ya tienes todo lo necesario para usar la API de Kick Shopping con Postman!**

Para más información técnica, consulta:

- [`README.md`](./README.md) - Documentación general
- [`API_REFERENCE.md`](./API_REFERENCE.md) - Referencia completa de endpoints
- [`SECURITY_GUIDE.md`](./SECURITY_GUIDE.md) - Guía de seguridad detallada
