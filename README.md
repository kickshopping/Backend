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
=========

# 👟 Kick Shopping - Backend API

Sistema de gestión integral para tienda de Indumentari desarrollado con **FastAPI** y **SQLAlchemy**. Proporciona una API REST completa para administrar todos los aspectos operativos de una tienda de ropa deportiva con autenticación JWT y sistema de permisos granulares.

## 🎯 Funcionalidad Principal

**Kick Shopping Backend** es una API REST que permite gestionar:

- **👥 Usuarios y Roles**: Sistema de autenticación JWT y autorización por permisos
- **🔒 Permisos**: Control granular de acceso por ruta y método HTTP
- **👟 Productos**: Catálogo de calzado deportivo y stock
- **🛒 Carrito de Compras**: Gestión del carrito de usuarios
- **🛡️ Seguridad**: Middleware de autenticación JWT con Bearer tokens

## 🏗️ Arquitectura del Sistema

```
📁 Backend/
├── 🚀 app.py                 # Aplicación principal FastAPI
├── 📊 kickshopping.db       # Base de datos SQLite
├── 📋 requirements.txt      # Dependencias Python
├── 🔧 config/               # Configuración del sistema
│   ├── basemodel.py         # Modelo base SQLAlchemy
│   ├── cnx.py              # Conexión a base de datos
│   └── associations.py     # Tablas intermedias
├── 🛡️ middlewares/         # Middleware de seguridad
│   └── auth.py             # Autenticación JWT
├── 🌱 seeders/             # Datos iniciales (ver README interno)
├── 📁 [módulos]/           # Módulos del sistema
│   ├── model.py            # Modelo de datos SQLAlchemy
│   ├── dto.py              # Data Transfer Objects
│   ├── services.py         # Lógica de negocio
│   └── routes.py           # Endpoints de la API
└── 📖 docs/                # Documentación
    ├── SECURITY_GUIDE.md   # Guía de seguridad y autenticación
    └── README.md           # Este archivo
```

## 🚀 Inicio Rápido

> 👋 **¿Primera vez?** Te recomendamos la [**Guía de Swagger UI**](./SWAGGER_GUIDE.md) para empezar rápidamente sin instalaciones adicionales.

### Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes Python)

### Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <url-repositorio>
   cd backend
   ```
2. **Crear entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```
3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar variables de entorno**:

   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```
5. **Cargar datos iniciales**:

   ```bash
   python ./seeders/seed_main.py
   ```
6. **Iniciar el servidor**:

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 5000
   ```
7. **Acceder a la documentación**:

   - Swagger UI: [http://localhost:5000/docs](http://localhost:5000/docs)
   - ReDoc: [http://localhost:5000/redoc](http://localhost:5000/redoc)

## 📚 Módulos del Sistema

| Módulo              | Descripción                          | Endpoints Principales                                                           |
| -------------------- | ------------------------------------- | ------------------------------------------------------------------------------- |
| **usuarios**   | Gestión de usuarios y autenticación | `GET /usuarios`, `POST /usuarios`, `POST /usuarios/login`                 |
| **roles**      | Administración de roles del sistema  | `GET /roles`, `POST /roles`, `PATCH /roles/{id}`                          |
| **permisos**   | Sistema de permisos granulares        | `GET /permisos`, `POST /permisos`, `POST /permisos/assign`                |
| **productos**  | Catálogo de calzado deportivo        | `GET /productos`, `POST /productos`, `PATCH /productos/{id}`              |
| **cart_items** | Gestión del carrito de compras       | `GET /cart_items/user/{id}`, `POST /cart_items`, `PATCH /cart_items/{id}` |

## 🔐 Seguridad y Autenticación

El sistema incluye un **middleware de autenticación JWT** completo con:

- ✅ Encriptación de contraseñas (bcrypt)
- ✅ Tokens JWT con expiración configurable (30 minutos por defecto)
- ✅ Sistema de permisos por rol, ruta y método HTTP
- ✅ Rutas públicas configurables (login, registro)
- ✅ Verificación automática de permisos
- ✅ Bearer token authentication con Swagger UI integrado

### 🚀 Cómo Autenticarse

#### **Opción 1: Usando Swagger UI** (Recomendado para desarrollo)

1. **Abrir Swagger**: [http://localhost:5000/docs](http://localhost:5000/docs)
2. **Hacer login**:

   - Buscar el endpoint `POST /usuarios/login`
   - Click en "Try it out"
   - Usar credenciales de prueba:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Ejecutar y copiar el `token` de la respuesta
3. **Configurar autenticación**:

   - Click en el botón **"Authorize"** 🔒 (esquina superior derecha)
   - Pegar el token en el campo de valor
   - Click en "Authorize" y luego "Close"
4. **¡Listo!** Ahora puedes usar todos los endpoints protegidos

#### **Opción 2: Usando Postman**

1. **Login** - `POST http://localhost:5000/usuarios/login`

   ```json
   {
     "username": "admin", 
     "password": "admin123"
   }
   ```
2. **Copiar token** de la respuesta
3. **Configurar Authorization**:

   - Type: **Bearer Token**
   - Token: `<tu-token-aqui>`

### 🔑 Respuesta de Login

El endpoint de login retorna:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "username": "admin"
}
```

### 📚 Guías de Uso Disponibles

- **🚀 [Guía de Swagger UI](./SWAGGER_GUIDE.md)** - Cómo usar la documentación interactiva
- **📮 [Guía de Postman](./POSTMAN_GUIDE.md)** - Configuración y uso con Postman
- **📋 [Referencia de API](./API_REFERENCE.md)** - Endpoints completos con ejemplos
- **🔒 [Guía de Seguridad](./SECURITY_GUIDE.md)** - Detalles técnicos de autenticación

## 🌱 Datos Iniciales (Seeders)

El sistema incluye seeders modulares para cargar datos de prueba:

- **Roles**: Administrador, Gerente, Empleado, Cliente
- **Usuarios**: Cuentas de prueba con contraseñas encriptadas
- **Permisos**: CRUD completo para todos los módulos
- **Productos**: Datos de ejemplo de calzado deportivo

**📖 Para información sobre seeders, consulta: [`./seeders/README.md`](./seeders/README.md)**

## 🛠️ Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno y rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para Python
- **[Pydantic](https://pydantic-docs.helpmanual.io/)**: Validación de datos
- **[JWT](https://jwt.io/)**: Autenticación con tokens
- **[bcrypt](https://pypi.org/project/bcrypt/)**: Encriptación de contraseñas
- **[SQLite](https://www.sqlite.org/)**: Base de datos ligera
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Gestión de variables de entorno

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Seguridad JWT
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Base de datos (opcional para SQLite)
DATABASE_URL=sqlite:///./kickshopping.db
```

### Estructura de Base de Datos

La base de datos incluye las siguientes tablas principales:

- `usuarios` - Información de usuarios del sistema
- `roles` - Roles disponibles (Administrador, Gerente, Empleado, Cliente)
- `permisos` - Permisos granulares por ruta y método
- `rol_permiso` - Tabla intermedia rol-permiso (many-to-many)
- `productos` - Catálogo de calzado deportivo
- `cart_items` - Elementos del carrito de compras

## 🧪 Testing y Desarrollo

### Usuarios de Prueba (después de ejecutar seeders)

| Usuario    | Contraseña | Rol           | Descripción               |
| ---------- | ----------- | ------------- | -------------------------- |
| admin      | admin123    | Administrador | Acceso completo al sistema |
| gerente01  | gerente123  | Gerente       | Gestión y supervisión    |
| empleado01 | empleado123 | Empleado      | Acceso operativo básico   |

### Comandos Útiles

```bash
# Ejecutar seeders completos
python ./seeders/seed_main.py

# Ejecutar seeder específico
python ./seeders/seed_roles.py

# Iniciar con recarga automática
uvicorn app:app --reload --host 0.0.0.0 --port 5000

# Ver documentación
curl http://localhost:5000/docs
```

### Características Técnicas

- ✅ **Modularidad** - Cada entidad tiene su propio módulo (model, dto, service, routes)
- ✅ **Seguridad JWT** - Tokens con expiración y roles/permisos granulares
- ✅ **Middleware personalizado** - Autenticación automática en rutas protegidas
- ✅ **Seeders organizados** - Datos de prueba modulares y reutilizables
- ✅ **Documentación automática** - Swagger UI y ReDoc incluidos
- ✅ **Validaciones** - DTOs con Pydantic
- ✅ **Manejo de errores** - Responses HTTP consistentes

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es desarrollado para fines educativos como parte del proyecto **Kick Shopping**.

---

**🚀 ¡Tu API REST está lista para producción con seguridad empresarial!**

# KickShopping Backend

## Descripción

Backend desarrollado con FastAPI, SQLAlchemy y SQLite para la gestión de usuarios, productos, roles, permisos y autenticación JWT.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

1. Clona el repositorio y navega a la carpeta `Backend-BackendBase`.
2. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

## Configuración

- Archivo `.env`:
  ```env
  ENVIROMENT=dev
  STRCNX=sqlite:///./kidkshopping.db
  SECRET_KEY=un_clave_secreta_segura
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  ```
- La base de datos se crea automáticamente como `kidkshopping.db` en la carpeta del backend.

## Ejecución

1. Inicia el servidor:
   ```powershell
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
2. Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints principales

- `/usuarios` CRUD de usuarios
- `/productos` CRUD de productos
- `/roles` CRUD de roles
- `/permisos` CRUD de permisos
- `/usuarios/login` Login y obtención de token JWT
- `/usuarios/me` Perfil del usuario autenticado

## Autenticación

- Usa JWT. El token se obtiene en `/usuarios/login` y se envía en el header `Authorization: Bearer <token>`.

## Seeders

- Para poblar la base de datos con datos de ejemplo, ejecuta los scripts en la carpeta `seeders`:
  ```powershell
  python seeders/seed_main.py
  ```

## Notas

- Si necesitas borrar todos los usuarios, puedes usar el endpoint DELETE `/usuarios/todos`.
- Para eliminar la tabla de usuarios completamente, usa DELETE `/usuarios/drop-table` (requiere token).

---
