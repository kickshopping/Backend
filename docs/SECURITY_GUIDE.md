# 📖 Sistema de Seguridad - Kick Shopping

Este documento explica cómo funciona el sistema de autenticación y autorización implementado.

## 🔐 CONFIGURACIÓN DE SEGURIDAD

### Rutas Públicas (No requieren autenticación):
- `/` - Página principal
- `/docs` - Documentación Swagger
- `/redoc` - Documentación ReDoc
- `/health` - Health check
- `/openapi.json` - Especificación OpenAPI

### Rutas con Métodos Públicos:
- `POST /usuarios` - Registro de nuevos usuarios
- `POST /usuarios/login` - Login de usuarios

### Rutas Protegidas:
- Todas las demás rutas requieren:
  1. Token JWT válido en header Authorization: "Bearer <token>"
  2. Permisos específicos del rol para la ruta y método HTTP

## 🛡️ FLUJO DE AUTENTICACIÓN

1. **Registro**: POST /usuarios (público)
   - Crea usuario con contraseña encriptada (bcrypt)
   - Asigna rol por defecto

2. **Login**: POST /usuarios/login (público)
   - Verifica usuario y contraseña
   - Devuelve JWT token con rol_id del usuario

3. **Acceso a rutas protegidas**:
   - Middleware verifica token JWT
   - Consulta permisos del rol en base de datos
   - Permite/deniega acceso según permisos

## 📋 CONFIGURACIÓN DE PERMISOS

Los permisos se configuran por:
- **Ruta**: URL normalizada (ej: /usuarios/{id})
- **Método**: GET, POST, PUT, DELETE, PATCH
- **Rol**: Cada rol tiene permisos específicos

## 🚀 CÓMO USAR EL SISTEMA

### Para desarrollo:
1. Ejecutar seeders: `python ./seeders/seed_main.py`
2. Iniciar servidor: `uvicorn app:app --reload`
3. Login con usuario de prueba
4. Usar token en header Authorization

### Para Frontend:
1. POST /usuarios/login con username/password
2. Guardar access_token del response
3. Enviar en todas las requests: 
   Authorization: "Bearer <access_token>"

## ⚙️ VARIABLES DE ENTORNO

Configurar en .env:
```
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🔧 ADMINISTRACIÓN

- Los permisos se gestionan en la tabla `permisos`
- Las asignaciones rol-permiso en `rol_permiso`
- Los seeders cargan permisos básicos de CRUD para cada módulo

**El middleware AuthMiddleware está habilitado y protegiendo todas las rutas automáticamente.**