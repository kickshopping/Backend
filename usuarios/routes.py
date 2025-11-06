from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .dto import UsuarioCreate, UsuarioOut, UsuarioUpdate, LoginResponse, LoginRequest
from .services import (
    get_all_usuarios,
    get_usuario_by_id,
    create_usuario,
    update_usuario,
    delete_usuario,
    login,
    decode_token,
    create_access_token,
    create_refresh_token,
)

usuarios = APIRouter()

# Bearer scheme para el token JWT
bearer_scheme = HTTPBearer()


# Endpoint para eliminar la tabla de usuarios (debe ir después de definir 'usuarios')
@usuarios.delete("/drop-table")
def eliminar_tabla_usuarios():
    try:
        from .services import drop_usuarios_table
        drop_usuarios_table()
        return {"detail": "Tabla de usuarios eliminada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@usuarios.get("", response_model=List[UsuarioOut])
def listar_usuarios():
    """Obtener todos los usuarios"""
    try:
        users = get_all_usuarios()
        if not users:
            return []
        return users
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener los usuarios"
        )


@usuarios.get("/me")
def leer_perfil(request: Request):
    """
    Devuelve los datos del usuario autenticado mediante el token JWT.
    El token ya fue validado por el AuthMiddleware.
    """
    user = request.state.user
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido: falta user_id")
    try:
        user_dict = get_usuario_by_id(user_id)
        return user_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado: {e}")


@usuarios.get("/{usu_id}", response_model=UsuarioOut)
def obtener_usuario(usu_id: int):
    """Obtener un usuario por ID"""
    try:
        usuario = get_usuario_by_id(usu_id)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


from fastapi import Request

@usuarios.post("", status_code=status.HTTP_201_CREATED)
async def crear_usuario(request: Request):
    """Crear un nuevo usuario con rol asignado y devolver token y user_id"""
    from .services import create_access_token
    try:
        body = await request.json()
        usu_usuario = body.get("email")
        usu_nombre_completo = f"{body.get('first_name','')} {body.get('last_name','')}".strip()
        usu_contrasenia = body.get("password")
        tipo_usuario = body.get("user_type", "Comprador")  # Si no se especifica, por defecto es Comprador
        birthdate = body.get("birthdate")
        usuario_data = {
            "usu_usuario": usu_usuario,
            "usu_nombre_completo": usu_nombre_completo,
            "usu_contrasenia": usu_contrasenia,
            "tipo_usuario": tipo_usuario,
            "birthdate": birthdate
        }
        from .dto import UsuarioCreate
        usuario_obj = UsuarioCreate(**usuario_data)
        nuevo_usuario = create_usuario(usuario_obj)
        access_token = create_access_token({
            "sub": nuevo_usuario.usu_usuario,
            "rol_id": nuevo_usuario.usu_rol_id,
            "user_id": nuevo_usuario.usu_id
        })
        refresh_token = create_refresh_token({
            "sub": nuevo_usuario.usu_usuario,
            "rol_id": nuevo_usuario.usu_rol_id,
            "user_id": nuevo_usuario.usu_id,
            "type": "refresh"
        })
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": nuevo_usuario.usu_id,
            "username": nuevo_usuario.usu_usuario
        }
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya existe"
        )


@usuarios.patch("/{usu_id}", response_model=UsuarioOut)
def actualizar_usuario(usu_id: int, update_data: UsuarioUpdate):
    """Actualizar datos de un usuario (nombre, contraseña, rol)"""
    try:
        return update_usuario(usu_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@usuarios.delete("/{usu_id}")
def eliminar_usuario(usu_id: int):
    """Eliminar un usuario por ID"""
    try:
        if delete_usuario(usu_id):
            return {"detail": f"Usuario {usu_id} eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@usuarios.post("/login", response_model=LoginResponse)
def login_usuario(login_data: LoginRequest):
    """Iniciar sesión con usuario y contraseña. Devuelve un JWT junto con el user_id y username."""
    return login(login_data.username, login_data.password)


@usuarios.post("/refresh")
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Renueva el access_token usando un refresh_token válido.
    En el cliente: guardar el refresh_token (localStorage o cookie segura) y enviarlo
    en Authorization: Bearer <refresh_token> a este endpoint.
    """
    token = credentials.credentials
    # Decodificar sin aceptar tokens que no sean refresh
    try:
        payload = decode_token(token)
    except HTTPException as e:
        raise e

    # El refresh token debe tener type == 'refresh'
    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail="Token suministrado no es refresh token")

    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=401, detail="Refresh token inválido: falta user_id")

    try:
        user_obj = get_usuario_by_id(user_id)
        user_type = None
        if isinstance(user_obj, dict):
            user_type = user_obj.get('rol_nombre')

        # Crear nuevo access token con el rol actual obtenido de la BD
        token_data = {
            "sub": payload.get('sub'),
            "rol_id": user_obj.get('usu_rol_id') if isinstance(user_obj, dict) else getattr(user_obj, 'usu_rol_id', None),
            "user_id": user_id,
            "username": user_obj.get('usu_usuario') if isinstance(user_obj, dict) else getattr(user_obj, 'usu_usuario', None),
            "user_type": user_type
        }
        access_token = create_access_token(token_data)

        # Refresh token con los mismos datos más el tipo
        refresh_token = create_refresh_token({
            **token_data,
            "type": "refresh"
        })

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_type": user_type,
            "user_id": user_id,
            "username": user_obj.get('usu_usuario')
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado: {e}")


# Endpoint para borrar todos los usuarios (top-level)
@usuarios.delete("/todos")
def borrar_todos_usuarios():
    try:
        from .services import delete_all_usuarios
        delete_all_usuarios()
        return {"detail": "Todos los usuarios han sido borrados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
